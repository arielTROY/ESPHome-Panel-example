#!/bin/bash
# Fix script to run inside the Docker container

echo "=== Applying atopile/faebryk fixes ==="

# Disable telemetry
export ATOPILE_TELEMETRY=false
export DO_NOT_TRACK=1

# Pre-configure atopile to skip interactive prompts
export ATOPILE_NO_INTERACTIVE=1
export ATOPILE_SKIP_KICAD_PLUGIN=1
export ATO_CI=1

# Ensure Python can import our sitecustomize patch (located in repo root)
export PYTHONPATH="/github/workspace:${PYTHONPATH}"

# -----------------------------------------------------------------------------
# Pre-configure atopile to avoid first-run wizard and KiCAD plugin prompt
# -----------------------------------------------------------------------------
echo "=== Pre-configuring atopile ==="
mkdir -p ~/.config/atopile

# Create a complete config file that marks first run as complete
cat > ~/.config/atopile/config.yaml << EOF
telemetry: false
id: ci-runner-$(uuidgen || echo "disabled")
kicad_plugin_installed: true
first_run_complete: true
analytics_enabled: false
EOF

# Also create the atopile cache directory to avoid any initialization issues
mkdir -p ~/.cache/atopile

# -----------------------------------------------------------------------------
# Copy sitecustomize.py into every uv-managed site-packages directory so that it
# is *always* discoverable, even if PYTHONPATH gets wiped by uv or pipx.
# -----------------------------------------------------------------------------
if [ -f "/github/workspace/sitecustomize.py" ]; then
  echo "=== Propagating sitecustomize.py into uv site-packages ==="
  # Iterate over all potential python versions inside the uv tool dir
  while IFS= read -r pkg_dir; do
    echo "Copying sitecustomize.py to: $pkg_dir"
    cp /github/workspace/sitecustomize.py "$pkg_dir/sitecustomize.py" || true
  done < <(find /root/.local/share/uv/tools -type d -name "site-packages" 2>/dev/null)
else
  echo "WARNING: sitecustomize.py not found in workspace – dataclass YAML fix will be unavailable"
fi

# Continue with telemetry config pre-seed so TelemetryConfig.load() never tries
# to write the file (avoids dataclass serialisation path entirely).
# This is redundant with the above but kept for compatibility
mkdir -p ~/.config/atopile
cat > ~/.config/atopile/config.yaml << EOF
telemetry: false
id: ci-runner-disabled
kicad_plugin_installed: true
first_run_complete: true
analytics_enabled: false
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