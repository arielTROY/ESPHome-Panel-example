# Bug Report: Multiple AttributeError issues in atopile/faebryk

## Summary
There are multiple bugs in the atopile/faebryk package causing AttributeError exceptions when trying to install dependencies.

## Environment
- atopile version: Latest (from Docker image ghcr.io/atopile/atopile-kicad:latest)
- Python version: 3.13
- OS: Linux (GitHub Actions ubuntu-latest)

## Bugs Found

### Bug 1: TelemetryConfig serialization error
```
RepresenterError: cannot represent an object: TelemetryConfig(telemetry=True, id=UUID('...'))
```

**Location**: `/atopile/telemetry.py:87`
**Issue**: The `yaml.dump(config, f)` call fails because TelemetryConfig is a dataclass that needs to be converted to a dict before serialization.

**Fix**:
```python
# Change this:
yaml.dump(config, f)
# To this:
from dataclasses import asdict
yaml.dump(asdict(config), f)
```

### Bug 2: InvalidPackageIdentifierError missing 'message' attribute
```
AttributeError: 'InvalidPackageIdentifierError' object has no attribute 'message'
```

**Location**: `/faebryk/libs/project/dependencies.py:298`
**Issue**: The error handler assumes all exceptions have a `message` attribute.

**Fix**:
```python
# Change this:
error_list = [f"{e.identifier}: {e.message}" for e in acc_errors]
# To this:
error_list = [f"{e.identifier}: {getattr(e, 'message', str(e))}" for e in acc_errors]
```

### Bug 3: PackagesApiHTTPError missing 'message' attribute
```
AttributeError: 'PackagesApiHTTPError' object has no attribute 'message'
```

**Location**: Same as Bug 2
**Issue**: Same as Bug 2 - the exception class doesn't have a `message` attribute.

## Steps to Reproduce
1. Create an atopile project with dependencies
2. Run `atopile install`
3. Observe the errors

## Workaround
1. Disable telemetry by creating `~/.config/atopile/config.yaml` with:
   ```yaml
   telemetry: false
   ```
2. Manually patch the faebryk package to fix the AttributeError issues

## Impact
These bugs prevent users from installing dependencies and building atopile projects, making the tool unusable in many cases.