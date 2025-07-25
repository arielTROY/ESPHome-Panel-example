#!/usr/bin/env python3
"""
Targeted fix for the specific InvalidPackageIdentifierError issue in atopile CI build.
"""

import os
import glob
import re
import sys

def fix_dependencies_error():
    """Fix the specific error in dependencies.py line 298"""
    print("=== Fixing dependencies.py error handling ===")
    
    # Find dependencies.py files
    patterns = [
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk/libs/project/dependencies.py",
        "/usr/local/lib/python*/site-packages/faebryk/libs/project/dependencies.py",
        "/opt/hostedtoolcache/Python/*/x64/lib/python*/site-packages/faebryk/libs/project/dependencies.py",
    ]
    
    deps_files = []
    for pattern in patterns:
        deps_files.extend(glob.glob(pattern))
    
    if not deps_files:
        print("No dependencies.py files found to patch")
        return False
    
    success = False
    for df in deps_files:
        print(f"Processing: {df}")
        try:
            with open(df, "r") as f:
                lines = f.readlines()
            
            # Find and fix line 298 or similar error list construction
            modified = False
            for i, line in enumerate(lines):
                # Look for the problematic line
                if "error_list = [" in line and "e.message" in line:
                    # Replace e.message with proper error handling
                    original_line = line
                    line = re.sub(
                        r'e\.message',
                        r'getattr(e, "message", getattr(e, "error", str(e)))',
                        line
                    )
                    if line != original_line:
                        lines[i] = line
                        modified = True
                        print(f"  Fixed line {i+1}: error_list construction")
                
                # Also check for f-string patterns
                elif 'f"{e.identifier}: {e.message}"' in line:
                    original_line = line
                    line = line.replace(
                        'f"{e.identifier}: {e.message}"',
                        'f"{e.identifier}: {getattr(e, \'message\', getattr(e, \'error\', str(e)))}"'
                    )
                    if line != original_line:
                        lines[i] = line
                        modified = True
                        print(f"  Fixed line {i+1}: f-string error formatting")
            
            # Write back if modified
            if modified:
                with open(df, "w") as f:
                    f.writelines(lines)
                print(f"  Successfully patched: {df}")
                success = True
            else:
                print(f"  No changes needed: {df}")
                
        except Exception as e:
            print(f"  Error processing {df}: {e}")
    
    return success

def disable_telemetry():
    """Disable telemetry to avoid serialization errors"""
    print("=== Disabling telemetry ===")
    
    # Set environment variables
    os.environ['ATOPILE_TELEMETRY'] = 'false'
    os.environ['ATOPILE_NO_TELEMETRY'] = '1'
    os.environ['DO_NOT_TRACK'] = '1'
    
    # Create config file
    config_dir = os.path.expanduser("~/.config/atopile")
    os.makedirs(config_dir, exist_ok=True)
    
    config_file = os.path.join(config_dir, "config.yaml")
    with open(config_file, "w") as f:
        f.write("telemetry: false\n")
        f.write("id: disabled\n")
    
    print(f"  Created config at: {config_file}")
    print("  Set environment variables")
    
    return True

def main():
    print("Targeted Fix for Atopile CI Build Errors")
    print("=" * 50)
    
    # First disable telemetry
    disable_telemetry()
    
    # Then fix the dependencies error
    if fix_dependencies_error():
        print("\nSuccessfully applied fixes!")
    else:
        print("\nWarning: Could not find files to patch")
        print("The error might occur during runtime")
    
    print("\nYou can now run atopile commands.")

if __name__ == "__main__":
    main()