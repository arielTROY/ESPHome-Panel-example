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
    try:
        for site_dir in site.getsitepackages():
            possible_paths.append(os.path.join(site_dir, "faebryk"))
    except:
        pass
    
    # Check user site-packages
    try:
        user_site = site.getusersitepackages()
        if user_site:
            possible_paths.append(os.path.join(user_site, "faebryk"))
    except:
        pass
    
    # Check UV tools location (more comprehensive patterns)
    uv_patterns = [
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk",
        "/root/.local/share/uv/tools/*/lib/python*/site-packages/faebryk",
        os.path.expanduser("~/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk"),
        os.path.expanduser("~/.local/share/uv/tools/*/lib/python*/site-packages/faebryk"),
    ]
    
    for pattern in uv_patterns:
        try:
            possible_paths.extend(glob.glob(pattern))
        except:
            pass
    
    # Check virtual environment locations
    venv_patterns = [
        "venv/lib/python*/site-packages/faebryk",
        ".venv/lib/python*/site-packages/faebryk",
        "env/lib/python*/site-packages/faebryk",
    ]
    
    for pattern in venv_patterns:
        try:
            possible_paths.extend(glob.glob(pattern))
        except:
            pass
    
    # Also check common system locations
    system_patterns = [
        "/usr/local/lib/python*/site-packages/faebryk",
        "/usr/lib/python*/site-packages/faebryk",
    ]
    
    for pattern in system_patterns:
        try:
            possible_paths.extend(glob.glob(pattern))
        except:
            pass
    
    # Return existing paths
    return [p for p in possible_paths if os.path.exists(p)]

def patch_dependencies_file(faebryk_path):
    """Patch the dependencies.py file to fix AttributeError issues."""
    deps_file = os.path.join(faebryk_path, "libs", "project", "dependencies.py")
    
    if not os.path.exists(deps_file):
        print(f"Dependencies file not found at: {deps_file}")
        return False
    
    print(f"Found dependencies.py at: {deps_file}")
    
    try:
        # Read the file
        with open(deps_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Create backup
    backup_path = deps_file + ".backup"
    if not os.path.exists(backup_path):
        try:
            with open(backup_path, 'w') as f:
                f.write(content)
            print(f"Created backup at: {backup_path}")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
    
    original_content = content
    
    # Fix 1: More comprehensive fix for error message handling
    # Look for the specific error_list line that's causing issues
    error_list_pattern = r'error_list\s*=\s*\[f["\']([^"\']*){e\.identifier}[^"\']*{e\.message}[^"\']*["\']'
    if re.search(error_list_pattern, content):
        content = re.sub(
            error_list_pattern,
            r'error_list = [f"\1{e.identifier}: {getattr(e, \'message\', getattr(e, \'error\', str(e)))}" for e in acc_errors]',
            content
        )
        print("Applied fix for error_list comprehension")
    
    # Fix 2: Generic fix for any remaining e.message references
    if "e.message" in content:
        content = re.sub(
            r'(\w+)\.message\b',
            r'getattr(\1, "message", getattr(\1, "error", str(\1)))',
            content
        )
        print("Applied generic fix for .message attributes")
    
    # Fix 3: Specific pattern for the line 298 error
    if "for e in acc_errors" in content:
        # Replace any pattern like f"{e.identifier}: {e.message}"
        content = re.sub(
            r'f["\']([^"\']*){e\.identifier}([^"\']*){e\.message}([^"\']*)["\']',
            r'f"\1{e.identifier}\2{getattr(e, \'message\', getattr(e, \'error\', str(e)))}\3"',
            content
        )
        print("Applied specific fix for error formatting")
    
    # Write the patched content if changes were made
    if content != original_content:
        try:
            with open(deps_file, 'w') as f:
                f.write(content)
            print("Successfully patched dependencies.py!")
            return True
        except Exception as e:
            print(f"Error writing patched file: {e}")
            return False
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
        "/root/.local/share/uv/tools/*/lib/python*/site-packages/atopile",
    ]
    
    # Expand glob patterns
    expanded_patterns = []
    for pattern in atopile_patterns:
        if '*' in pattern:
            try:
                expanded_patterns.extend(glob.glob(pattern))
            except:
                pass
        else:
            expanded_patterns.append(pattern)
    
    for atopile_path in expanded_patterns:
        telemetry_file = os.path.join(atopile_path, "telemetry.py")
        if os.path.exists(telemetry_file):
            print(f"Found telemetry.py at: {telemetry_file}")
            
            try:
                with open(telemetry_file, 'r') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading telemetry file: {e}")
                continue
            
            # Create backup
            backup_path = telemetry_file + ".backup"
            if not os.path.exists(backup_path):
                try:
                    with open(backup_path, 'w') as f:
                        f.write(content)
                    print(f"Created telemetry backup at: {backup_path}")
                except Exception as e:
                    print(f"Warning: Could not create telemetry backup: {e}")
            
            original_content = content
            
            # Fix 1: Add dataclasses import if needed
            if ("yaml.dump(config, f)" in content and 
                "from dataclasses import asdict" not in content and
                "import dataclasses" not in content):
                
                # Find the best place to add the import
                lines = content.split('\n')
                import_added = False
                
                # Look for existing imports
                for i, line in enumerate(lines):
                    if (line.strip().startswith('from ') or 
                        line.strip().startswith('import ')) and not import_added:
                        # Continue to find the last import
                        continue
                    elif (i > 0 and not line.strip() and 
                          i > 0 and (lines[i-1].startswith('from ') or lines[i-1].startswith('import '))):
                        # Insert after imports block
                        lines.insert(i, 'from dataclasses import asdict')
                        import_added = True
                        break
                
                if not import_added:
                    # If no good place found, add after the first few lines
                    lines.insert(3, 'from dataclasses import asdict')
                
                content = '\n'.join(lines)
                print("Added dataclasses import")
            
            # Fix 2: Replace yaml.dump(config, f) with safe version
            if "yaml.dump(config, f)" in content:
                content = re.sub(
                    r'yaml\.dump\(config,\s*f\)',
                    'yaml.dump(asdict(config) if hasattr(config, "__dataclass_fields__") else config, f)',
                    content
                )
                print("Fixed yaml.dump to handle dataclass serialization")
            
            # Write back if changed
            if content != original_content:
                try:
                    with open(telemetry_file, 'w') as f:
                        f.write(content)
                    print("Successfully patched telemetry.py!")
                    return True
                except Exception as e:
                    print(f"Error writing patched telemetry file: {e}")
    
    return False

def main():
    print("Atopile/Faebryk Error Fix Script")
    print("=" * 50)
    
    # Find faebryk installations
    faebryk_paths = find_faebryk_files()
    
    if not faebryk_paths:
        print("ERROR: Could not find faebryk installation")
        print("\nSearched in common locations:")
        print("- site-packages directories")
        print("- UV tools directories")
        print("- Virtual environments")
        print("- System directories")
        print("\nPlease make sure atopile/faebryk is installed.")
        print("You can also run this script with the path to faebryk as an argument.")
        
        # Try to provide more debugging info
        print("\nDebugging info:")
        try:
            import faebryk
            print(f"faebryk module found at: {faebryk.__file__}")
            faebryk_dir = os.path.dirname(faebryk.__file__)
            print(f"Attempting to patch: {faebryk_dir}")
            if patch_dependencies_file(faebryk_dir):
                print("Successfully patched using module location!")
                return
        except ImportError:
            print("faebryk module not importable")
        
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