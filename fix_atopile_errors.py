#!/usr/bin/env python3
"""
Fix script for atopile/faebryk errors.
This script patches multiple issues in the faebryk package.
"""

import os
import sys
import re
import glob
import site
from pathlib import Path

def find_faebryk_files():
    """Find all faebryk installation locations."""
    possible_paths = []
    
    # Check site-packages locations
    for site_dir in site.getsitepackages():
        possible_paths.append(os.path.join(site_dir, "faebryk"))
    
    # Check user site-packages
    user_site = site.getusersitepackages()
    if user_site:
        possible_paths.append(os.path.join(user_site, "faebryk"))
    
    # Check UV tools location
    uv_patterns = [
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk",
        os.path.expanduser("~/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk"),
    ]
    
    for pattern in uv_patterns:
        possible_paths.extend(glob.glob(pattern))
    
    # Check virtual environment locations
    venv_patterns = [
        "venv/lib/python*/site-packages/faebryk",
        ".venv/lib/python*/site-packages/faebryk",
        "env/lib/python*/site-packages/faebryk",
    ]
    
    for pattern in venv_patterns:
        possible_paths.extend(glob.glob(pattern))
    
    # Return existing paths
    return [p for p in possible_paths if os.path.exists(p)]

def patch_dependencies_file(faebryk_path):
    """Patch the dependencies.py file to fix AttributeError issues."""
    deps_file = os.path.join(faebryk_path, "libs", "project", "dependencies.py")
    
    if not os.path.exists(deps_file):
        print(f"Dependencies file not found at: {deps_file}")
        return False
    
    print(f"Found dependencies.py at: {deps_file}")
    
    # Read the file
    with open(deps_file, 'r') as f:
        content = f.read()
    
    # Create backup
    backup_path = deps_file + ".backup"
    if not os.path.exists(backup_path):
        with open(backup_path, 'w') as f:
            f.write(content)
        print(f"Created backup at: {backup_path}")
    
    original_content = content
    
    # Fix 1: InvalidPackageIdentifierError.message -> str(e)
    patterns = [
        (r'f"{e\.identifier}:\s*{e\.message}"', 'f"{e.identifier}: {str(e)}"'),
        (r'e\.message', 'getattr(e, "message", str(e))'),
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"Applied fix for pattern: {pattern}")
    
    # Fix 2: PackagesApiHTTPError.message -> str(e) or e.error
    # Look for error handling code that might reference e.message
    if "PackagesApiHTTPError" in content or "e.message" in content:
        # Replace any remaining e.message with a safe alternative
        content = re.sub(
            r'(\w+)\.message\b',
            r'getattr(\1, "message", getattr(\1, "error", str(\1)))',
            content
        )
        print("Applied generic fix for .message attributes")
    
    # Fix 3: Specific fix for the error list comprehension at line 298
    if "error_list = [" in content and "e.message" in content:
        # Find and fix the specific line causing issues
        content = re.sub(
            r'error_list\s*=\s*\[f"{e\.identifier}:\s*{e\.message}"',
            'error_list = [f"{e.identifier}: {getattr(e, \'message\', getattr(e, \'error\', str(e)))}"',
            content
        )
        print("Applied specific fix for error_list comprehension")
    
    # Write the patched content if changes were made
    if content != original_content:
        with open(deps_file, 'w') as f:
            f.write(content)
        print("Successfully patched the file!")
        return True
    else:
        print("No changes needed or already patched.")
        return False

def patch_telemetry_file(faebryk_path):
    """Patch telemetry issues if atopile is installed."""
    # Try to find atopile installation
    atopile_patterns = [
        os.path.join(os.path.dirname(faebryk_path), "atopile"),
        os.path.join(os.path.dirname(os.path.dirname(faebryk_path)), "atopile"),
        # Also check UV tools location
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/atopile",
    ]
    
    # Expand glob patterns
    expanded_patterns = []
    for pattern in atopile_patterns:
        if '*' in pattern:
            expanded_patterns.extend(glob.glob(pattern))
        else:
            expanded_patterns.append(pattern)
    
    for atopile_path in expanded_patterns:
        telemetry_file = os.path.join(atopile_path, "telemetry.py")
        if os.path.exists(telemetry_file):
            print(f"Found telemetry.py at: {telemetry_file}")
            
            with open(telemetry_file, 'r') as f:
                content = f.read()
            
            # Create backup
            backup_path = telemetry_file + ".backup"
            if not os.path.exists(backup_path):
                with open(backup_path, 'w') as f:
                    f.write(content)
            
            original_content = content
            
            # Fix 1: Add dataclasses import if needed
            if "yaml.dump(config, f)" in content and "from dataclasses import asdict" not in content:
                # Add import at the top of the file after other imports
                import_added = False
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('from ') or line.startswith('import '):
                        # Find the last import line
                        continue
                    elif i > 0 and not line.strip() and not import_added:
                        # Insert after imports
                        lines.insert(i, 'from dataclasses import asdict')
                        import_added = True
                        break
                
                if not import_added:
                    # If no imports found, add at the beginning
                    lines.insert(0, 'from dataclasses import asdict')
                
                content = '\n'.join(lines)
                print("Added dataclasses import")
            
            # Fix 2: Replace yaml.dump(config, f) with yaml.dump(asdict(config), f)
            if "yaml.dump(config, f)" in content:
                content = re.sub(
                    r'yaml\.dump\(config,\s*f\)',
                    'yaml.dump(asdict(config) if hasattr(config, "__dataclass_fields__") else config, f)',
                    content
                )
                print("Fixed yaml.dump to handle dataclass serialization")
            
            # Fix 3: Add a custom representer for TelemetryConfig if needed
            if "TelemetryConfig" in content and "yaml_representer" not in content:
                # Add a custom representer after the class definition
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'class TelemetryConfig' in line:
                        # Find the end of the class
                        indent_level = len(line) - len(line.lstrip())
                        j = i + 1
                        while j < len(lines) and (lines[j].strip() == '' or 
                                                 (lines[j].strip() != '' and 
                                                  len(lines[j]) - len(lines[j].lstrip()) > indent_level)):
                            j += 1
                        
                        # Insert the representer after the class
                        representer_code = '''
# Add YAML representer for TelemetryConfig
def telemetry_config_representer(dumper, data):
    return dumper.represent_dict(asdict(data) if hasattr(data, "__dataclass_fields__") else data.__dict__)

try:
    from ruamel.yaml import YAML
    YAML.add_representer(TelemetryConfig, telemetry_config_representer)
except:
    pass
'''
                        lines.insert(j, representer_code)
                        content = '\n'.join(lines)
                        print("Added custom YAML representer for TelemetryConfig")
                        break
            
            # Write back if changed
            if content != original_content:
                with open(telemetry_file, 'w') as f:
                    f.write(content)
                print("Patched telemetry.py")
                return True
    
    return False

def main():
    print("Atopile/Faebryk Error Fix Script")
    print("=" * 50)
    
    # Find faebryk installations
    faebryk_paths = find_faebryk_files()
    
    if not faebryk_paths:
        print("ERROR: Could not find faebryk installation")
        print("\nPlease make sure atopile/faebryk is installed.")
        print("You can also run this script with the path to faebryk as an argument.")
        sys.exit(1)
    
    print(f"Found {len(faebryk_paths)} faebryk installation(s)")
    
    # Patch each installation
    success_count = 0
    for faebryk_path in faebryk_paths:
        print(f"\nProcessing: {faebryk_path}")
        if patch_dependencies_file(faebryk_path):
            success_count += 1
        
        # Also try to patch telemetry
        patch_telemetry_file(faebryk_path)
    
    if success_count > 0:
        print(f"\nSuccessfully patched {success_count} installation(s)!")
        print("You should now be able to run atopile without AttributeError.")
    else:
        print("\nNo installations were patched. They may already be fixed.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allow manual specification of the faebryk directory
        faebryk_path = sys.argv[1]
        if os.path.exists(faebryk_path):
            patch_dependencies_file(faebryk_path)
            patch_telemetry_file(faebryk_path)
        else:
            print(f"ERROR: Path not found: {faebryk_path}")
    else:
        main()