# CI Build Error Fix for ESPHome-Panel-example

## Problem Description

The GitHub Actions CI build is failing with two main errors:

1. **Telemetry Serialization Error**: 
   ```
   RepresenterError: cannot represent an object: TelemetryConfig(telemetry=True, id=UUID('...'))
   ```
   This occurs because the `TelemetryConfig` dataclass cannot be serialized by the YAML dumper.

2. **AttributeError in Dependencies**:
   ```
   AttributeError: 'PackagesApiHTTPError' object has no attribute 'message'
   ```
   This happens when the error handling code tries to access a non-existent `message` attribute.

## Solutions

I've created three different workflow files to address these issues:

### 1. Simple Solution - Disable Telemetry (`ci-simple.yml`)
The easiest fix is to disable telemetry entirely:
- Sets environment variables to disable telemetry
- Creates a config file that disables telemetry
- This avoids the serialization issue completely

### 2. Patch Solution - Fix the Code (`ci-fixed.yml`)
This approach patches the problematic code directly:
- Runs inline Python code to fix the telemetry serialization
- Patches the error handling in dependencies.py
- More robust but requires modifying the installed packages

### 3. Original Workflow with Fix Script (`ci.yml`)
Updated the original workflow to run the fix script:
- Uses the existing `fix_atopile_errors.py` script
- Applies patches before running atopile install

## How to Use

1. **For Quick Fix**: Use the `ci-simple.yml` workflow
   ```bash
   # In your GitHub Actions, use:
   .github/workflows/ci-simple.yml
   ```

2. **For Comprehensive Fix**: Use the `ci-fixed.yml` workflow
   ```bash
   # This applies all patches and handles edge cases
   .github/workflows/ci-fixed.yml
   ```

3. **To Test Locally**: Run the fix script
   ```bash
   python3 fix_atopile_errors.py
   ```

## Root Cause

The issues stem from:
1. The atopile telemetry system trying to serialize a dataclass without proper YAML representation
2. The faebryk error handling assuming error objects have a `message` attribute when they might have `error` or other attributes

These are upstream bugs in the atopile/faebryk packages that should be reported to their maintainers.

## Recommended Action

1. Use the `ci-simple.yml` workflow for now (disables telemetry)
2. Report these issues to the atopile project
3. Once fixed upstream, you can switch back to the standard Docker action

## Testing

To test if the fix works:
```bash
# Run locally with Docker
docker run --rm \
  -v $(pwd):/github/workspace \
  -w /github/workspace \
  -e ATOPILE_TELEMETRY=false \
  ghcr.io/atopile/atopile-kicad:latest \
  atopile install
```