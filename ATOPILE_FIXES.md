# Atopile Error Fixes

This document describes the fixes implemented to resolve critical errors in the atopile/faebryk package that were preventing successful builds.

## Issues Fixed

### 1. TelemetryConfig Serialization Error

**Error:**
```
RepresenterError: cannot represent an object: TelemetryConfig(telemetry=True, id=UUID('...'))
```

**Root Cause:** The `TelemetryConfig` dataclass cannot be directly serialized to YAML because it contains complex objects like UUIDs.

**Fix:** 
- Added `from dataclasses import asdict` import
- Modified `yaml.dump(config, f)` to `yaml.dump(asdict(config), f)`
- Created telemetry config file to disable telemetry: `~/.config/atopile/config.yaml`

### 2. InvalidPackageIdentifierError AttributeError

**Error:**
```
AttributeError: 'InvalidPackageIdentifierError' object has no attribute 'message'
```

**Root Cause:** The error handling code assumes all exception objects have a `message` attribute, but some exception classes don't provide this.

**Fix:** 
- Replaced `e.message` with `getattr(e, 'message', getattr(e, 'error', str(e)))`
- This provides a fallback chain: try `message`, then `error`, then string representation

## Fix Scripts

### 1. `inline_fix.py`
A comprehensive fix script that can be run directly in the Docker container. It:
- Creates telemetry configuration to disable telemetry
- Patches telemetry.py files to fix YAML serialization
- Patches dependencies.py files to fix AttributeError issues

### 2. `docker_fix_atopile.py`
A specialized version designed specifically for Docker container environments.

### 3. `fix_atopile_errors.py`
The original comprehensive fix script with enhanced error handling and path detection.

### 4. `Dockerfile.fixed`
A custom Dockerfile that extends the official atopile image and applies all necessary fixes.

## GitHub Actions Workflows

### Updated `ci.yml`
- Uses the `inline_fix.py` script for reliable fixing
- Includes comprehensive error handling and fallback strategies
- Adds telemetry disabling environment variables

### New `build-with-fixed-image.yml`
- Builds a custom Docker image with fixes pre-applied
- Provides a more reliable build environment
- Separates the fix process from the build process

## Usage

### Quick Fix (Recommended)
Run the inline fix script in your Docker container:
```bash
python3 inline_fix.py
```

### Custom Docker Image
Build and use the fixed Docker image:
```bash
docker build -f Dockerfile.fixed -t atopile-fixed .
docker run --rm -v $(pwd):/workspace -w /workspace atopile-fixed atopile install
```

### Manual Fix
If you need to apply fixes manually:

1. **Disable Telemetry:**
   ```bash
   mkdir -p ~/.config/atopile
   echo "telemetry: false" > ~/.config/atopile/config.yaml
   ```

2. **Fix Dependencies File:**
   Find and edit `/path/to/faebryk/libs/project/dependencies.py`:
   ```python
   # Replace:
   error_list = [f"{e.identifier}: {e.message}" for e in acc_errors]
   # With:
   error_list = [f"{e.identifier}: {getattr(e, 'message', str(e))}" for e in acc_errors]
   ```

3. **Fix Telemetry File:**
   Find and edit `/path/to/atopile/telemetry.py`:
   ```python
   # Add at top:
   from dataclasses import asdict
   
   # Replace:
   yaml.dump(config, f)
   # With:
   yaml.dump(asdict(config), f)
   ```

## Environment Variables

Set these environment variables to help prevent issues:
- `ATOPILE_TELEMETRY=false` - Disable telemetry
- `ATO_CI=1` - Enable CI mode

## Testing

After applying fixes, test with:
```bash
atopile install
atopile build
```

Both commands should complete without AttributeError or RepresenterError exceptions.

## Notes

- These fixes are temporary workarounds for upstream issues
- The fixes should be applied each time you use a fresh Docker container
- Consider using the custom Docker image for consistent results
- Monitor the atopile project for official fixes to these issues