#!/usr/bin/env python3
"""
Docker container fix script for atopile/faebryk errors.
This script is designed to run inside the atopile Docker container.
"""

import os
import sys
import re
import glob
from pathlib import Path

def find_and_fix_faebryk():
    """Find and fix faebryk installation in Docker container."""
    
    # Common paths in Docker container
    search_paths = [
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk",
        "/usr/local/lib/python*/site-packages/faebryk",
        "/root/.local/lib/python*/site-packages/faebryk",
    ]
    
    faebryk_paths = []
    for pattern in search_paths:
        faebryk_paths.extend(glob.glob(pattern))
    
    if not faebryk_paths:
        print("ERROR: Could not find faebryk installation in container")
        return False
    
    success = False
    for faebryk_path in faebryk_paths:
        print(f"Processing faebryk at: {faebryk_path}")
        if fix_dependencies_file(faebryk_path):
            success = True
        if fix_telemetry_file(faebryk_path):
            success = True
    
    return success

def fix_dependencies_file(faebryk_path):
    """Fix the dependencies.py file."""
    deps_file = os.path.join(faebryk_path, "libs", "project", "dependencies.py")
    
    if not os.path.exists(deps_file):
        print(f"Dependencies file not found: {deps_file}")
        return False
    
    print(f"Fixing dependencies.py at: {deps_file}")
    
    try:
        with open(deps_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading dependencies file: {e}")
        return False
    
    original_content = content
    
    # Fix the specific error at line 298
    # Replace: error_list = [f"{e.identifier}: {e.message}" for e in acc_errors]
    # With: error_list = [f"{e.identifier}: {getattr(e, 'message', str(e))}" for e in acc_errors]
    
    patterns_to_fix = [
        # Pattern 1: Direct f-string with e.message
        (r'f"([^"]*){e\.identifier}([^"]*){e\.message}([^"]*)"', 
         r'f"\1{e.identifier}\2{getattr(e, \'message\', str(e))}\3"'),
        
        # Pattern 2: Any remaining e.message references
        (r'(\w+)\.message\b', 
         r'getattr(\1, "message", str(\1))'),
        
        # Pattern 3: Specific error_list comprehension
        (r'error_list\s*=\s*\[([^\]]*e\.message[^\]]*)\]',
         r'error_list = [f"{e.identifier}: {getattr(e, \'message\', str(e))}" for e in acc_errors]'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"Applied fix for pattern: {pattern[:50]}...")
    
    # Write the fixed content
    if content != original_content:
        try:
            with open(deps_file, 'w') as f:
                f.write(content)
            print("Successfully fixed dependencies.py!")
            return True
        except Exception as e:
            print(f"Error writing fixed file: {e}")
            return False
    else:
        print("Dependencies file already fixed or no changes needed.")
        return False

def fix_telemetry_file(faebryk_path):
    """Fix telemetry serialization issues."""
    
    # Find atopile installation relative to faebryk
    atopile_patterns = [
        os.path.join(os.path.dirname(faebryk_path), "atopile"),
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/atopile",
    ]
    
    atopile_paths = []
    for pattern in atopile_patterns:
        if '*' in pattern:
            atopile_paths.extend(glob.glob(pattern))
        else:
            atopile_paths.append(pattern)
    
    for atopile_path in atopile_paths:
        telemetry_file = os.path.join(atopile_path, "telemetry.py")
        if os.path.exists(telemetry_file):
            print(f"Fixing telemetry.py at: {telemetry_file}")
            
            try:
                with open(telemetry_file, 'r') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading telemetry file: {e}")
                continue
            
            original_content = content
            
            # Add dataclasses import if not present
            if ("yaml.dump(config, f)" in content and 
                "from dataclasses import asdict" not in content):
                
                # Find imports section and add the import
                lines = content.split('\n')
                
                # Look for the first non-import line to insert before it
                insert_idx = 0
                for i, line in enumerate(lines):
                    if line.strip() == '' or line.startswith('#'):
                        continue
                    elif line.startswith('from ') or line.startswith('import '):
                        insert_idx = i + 1
                    else:
                        break
                
                lines.insert(insert_idx, 'from dataclasses import asdict')
                content = '\n'.join(lines)
                print("Added dataclasses import")
            
            # Fix yaml.dump call
            if "yaml.dump(config, f)" in content:
                content = re.sub(
                    r'yaml\.dump\(config,\s*f\)',
                    'yaml.dump(asdict(config) if hasattr(config, "__dataclass_fields__") else config, f)',
                    content
                )
                print("Fixed yaml.dump call")
            
            # Write the fixed content
            if content != original_content:
                try:
                    with open(telemetry_file, 'w') as f:
                        f.write(content)
                    print("Successfully fixed telemetry.py!")
                    return True
                except Exception as e:
                    print(f"Error writing fixed telemetry file: {e}")
    
    return False

def create_telemetry_config():
    """Create telemetry config to disable telemetry."""
    config_dir = Path.home() / ".config" / "atopile"
    config_file = config_dir / "config.yaml"
    
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            f.write("telemetry: false\n")
        print(f"Created telemetry config at: {config_file}")
        return True
    except Exception as e:
        print(f"Error creating telemetry config: {e}")
        return False

def main():
    print("Docker Atopile Fix Script")
    print("=" * 40)
    
    # Create telemetry config first
    create_telemetry_config()
    
    # Find and fix faebryk installation
    if find_and_fix_faebryk():
        print("\nFixes applied successfully!")
        print("Atopile should now work without AttributeError issues.")
    else:
        print("\nNo fixes were applied.")
        print("The installation may already be fixed or not found.")

if __name__ == "__main__":
    main()