#!/usr/bin/env python3
"""
Inline fix for atopile/faebryk errors.
This script can be run directly in the Docker container to fix known issues.
"""

import os
import glob
import re
import sys

def fix_telemetry_files():
    """Fix telemetry serialization issues."""
    print("=== Fixing telemetry files ===")
    
    # Find telemetry.py files
    patterns = [
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/atopile/telemetry.py",
        "/usr/local/lib/python*/site-packages/atopile/telemetry.py",
    ]
    
    telemetry_files = []
    for pattern in patterns:
        telemetry_files.extend(glob.glob(pattern))
    
    if not telemetry_files:
        print("No telemetry files found")
        return False
    
    success = False
    for tf in telemetry_files:
        print(f"Processing: {tf}")
        try:
            with open(tf, "r") as f:
                content = f.read()
            
            original_content = content
            
            # Add asdict import if not present
            if ("yaml.dump(config, f)" in content and 
                "from dataclasses import asdict" not in content and
                "import dataclasses" not in content):
                
                # Find the best place to add import
                lines = content.split('\n')
                import_line = "from dataclasses import asdict"
                
                # Find last import line
                insert_idx = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith(('from ', 'import ')):
                        insert_idx = i + 1
                    elif line.strip() and not line.startswith('#'):
                        break
                
                lines.insert(insert_idx, import_line)
                content = '\n'.join(lines)
                print("  Added dataclasses import")
            
            # Fix yaml.dump call
            if "yaml.dump(config, f)" in content:
                content = re.sub(
                    r"yaml\.dump\(config,\s*f\)",
                    "yaml.dump(asdict(config) if hasattr(config, '__dataclass_fields__') else config, f)",
                    content
                )
                print("  Fixed yaml.dump call")
            
            # Write back if changed
            if content != original_content:
                with open(tf, "w") as f:
                    f.write(content)
                print(f"  Successfully patched: {tf}")
                success = True
            else:
                print(f"  No changes needed: {tf}")
                
        except Exception as e:
            print(f"  Error processing {tf}: {e}")
    
    return success

def fix_dependencies_files():
    """Fix dependencies.py AttributeError issues."""
    print("=== Fixing dependencies files ===")
    
    # Find dependencies.py files
    patterns = [
        "/root/.local/share/uv/tools/atopile/lib/python*/site-packages/faebryk/libs/project/dependencies.py",
        "/usr/local/lib/python*/site-packages/faebryk/libs/project/dependencies.py",
    ]
    
    deps_files = []
    for pattern in patterns:
        deps_files.extend(glob.glob(pattern))
    
    if not deps_files:
        print("No dependencies files found")
        return False
    
    success = False
    for df in deps_files:
        print(f"Processing: {df}")
        try:
            with open(df, "r") as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Generic .message attribute access
            if ".message" in content:
                content = re.sub(
                    r"(\w+)\.message\b",
                    r"getattr(\1, 'message', getattr(\1, 'error', str(\1)))",
                    content
                )
                print("  Fixed .message attribute access")
            
            # Fix 2: Specific error_list comprehension
            if "error_list = [" in content and "e.message" in content:
                # Look for the specific pattern that's causing issues
                content = re.sub(
                    r'f"([^"]*){e\.identifier}([^"]*){e\.message}([^"]*)"',
                    r'f"\1{e.identifier}\2{getattr(e, \'message\', getattr(e, \'error\', str(e)))}\3"',
                    content
                )
                print("  Fixed error_list f-string formatting")
            
            # Fix 3: Any remaining e.something.message patterns
            content = re.sub(
                r"([a-zA-Z_]\w*)\.([a-zA-Z_]\w*)\.message\b",
                r"getattr(\1.\2, 'message', getattr(\1.\2, 'error', str(\1.\2)))",
                content
            )
            
            # Write back if changed
            if content != original_content:
                with open(df, "w") as f:
                    f.write(content)
                print(f"  Successfully patched: {df}")
                success = True
            else:
                print(f"  No changes needed: {df}")
                
        except Exception as e:
            print(f"  Error processing {df}: {e}")
    
    return success

def create_telemetry_config():
    """Create telemetry config to disable telemetry."""
    print("=== Creating telemetry config ===")
    
    config_dir = os.path.expanduser("~/.config/atopile")
    config_file = os.path.join(config_dir, "config.yaml")
    
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, "w") as f:
            f.write("telemetry: false\n")
        print(f"Created telemetry config: {config_file}")
        return True
    except Exception as e:
        print(f"Error creating telemetry config: {e}")
        return False

def main():
    print("Atopile Inline Fix Script")
    print("=" * 40)
    
    # Create telemetry config
    create_telemetry_config()
    
    # Apply fixes
    telemetry_fixed = fix_telemetry_files()
    deps_fixed = fix_dependencies_files()
    
    if telemetry_fixed or deps_fixed:
        print("\n=== Fixes applied successfully! ===")
        if telemetry_fixed:
            print("✓ Telemetry serialization fixed")
        if deps_fixed:
            print("✓ Dependencies AttributeError fixed")
    else:
        print("\n=== No fixes were needed or applied ===")
    
    print("Atopile should now work without errors.")

if __name__ == "__main__":
    main()