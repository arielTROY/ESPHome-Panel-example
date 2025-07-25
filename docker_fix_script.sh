#!/bin/bash
# Fix script to run inside the Docker container

echo "=== Applying atopile/faebryk fixes ==="

# Disable telemetry
export ATOPILE_TELEMETRY=false
export DO_NOT_TRACK=1

# Ensure Python can import our sitecustomize patch (located in repo root)
export PYTHONPATH="/github/workspace:${PYTHONPATH}"
mkdir -p ~/.config/atopile
cat > ~/.config/atopile/config.yaml << EOF
telemetry: false
id: disabled
EOF

# Find and patch the dependencies.py file
echo "=== Looking for faebryk dependencies.py ==="
DEPS_FILE=$(find /root/.local/share/uv/tools -name "dependencies.py" -path "*/faebryk/libs/project/*" 2>/dev/null | head -1)

if [ -n "$DEPS_FILE" ]; then
    echo "Found dependencies.py at: $DEPS_FILE"
    
    # Create backup
    cp "$DEPS_FILE" "$DEPS_FILE.backup"
    
    # Apply the fix using sed
    # Replace e.message with a safe accessor
    sed -i 's/e\.message/getattr(e, "message", getattr(e, "error", str(e)))/g' "$DEPS_FILE"
    
    # Also fix the specific line 298 pattern
    sed -i 's/{e\.identifier}: {e\.message}/{e.identifier}: {getattr(e, "message", getattr(e, "error", str(e)))}/g' "$DEPS_FILE"
    
    echo "Applied fixes to dependencies.py"
else
    echo "WARNING: Could not find dependencies.py to patch"
fi

# Find and patch telemetry.py
echo "=== Looking for atopile telemetry.py ==="
TELEMETRY_FILE=$(find /root/.local/share/uv/tools -name "telemetry.py" -path "*/atopile/*" 2>/dev/null | head -1)

if [ -n "$TELEMETRY_FILE" ]; then
    echo "Found telemetry.py at: $TELEMETRY_FILE"
    
    # Check if it needs the dataclass fix
    if grep -q "yaml.dump(config, f)" "$TELEMETRY_FILE" && ! grep -q "from dataclasses import asdict" "$TELEMETRY_FILE"; then
        # Add the import at the top after other imports
        sed -i '1,/^import\|^from/ {/^import\|^from/!b; :a; n; /^import\|^from/ba; i\from dataclasses import asdict
        }' "$TELEMETRY_FILE"
        
        # Replace yaml.dump to handle dataclasses
        sed -i 's/yaml\.dump(config, f)/yaml.dump(asdict(config) if hasattr(config, "__dataclass_fields__") else config, f)/g' "$TELEMETRY_FILE"
        
        echo "Applied telemetry dataclass fix"
    fi
fi

echo "=== Fixes applied, proceeding with atopile ==="