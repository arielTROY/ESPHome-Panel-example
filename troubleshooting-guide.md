# Troubleshooting Guide: atopile-kicad GitHub Actions Error

## Error Description
```
ERROR    Configuration Error                                         
         Unable to extract tag using discriminator 'type':           
         `dependencies`
```

## Root Cause
The `atopile-kicad` Docker image appears to be using a different version of atopile than what's specified in your `ato.yaml` file. The error suggests it's expecting a different configuration schema for dependencies.

## Solutions

### Solution 1: Check Docker Image Version
The workflow is using `ghcr.io/atopile/atopile-kicad:latest` which might have breaking changes. Try pinning to a specific version:

1. Check available versions at: https://github.com/atopile/atopile/pkgs/container/atopile-kicad
2. Update `.github/workflows/ci.yml` to use a specific version

### Solution 2: Update atopile Version
Your `ato.yaml` specifies `requires-atopile: ^0.2.0`. The Docker image might be using a newer version. Try:

```yaml
requires-atopile: ^0.3.0
```

### Solution 3: Verify Dependencies Format
Ensure your dependencies are in the correct format. The current format appears correct:
```yaml
dependencies:
- package@commit_hash
- package-name
```

### Solution 4: Check for Syntax Issues
Make sure there are no hidden characters or formatting issues in `ato.yaml`. The error might be misleading.

### Solution 5: Local Testing
Test the build locally using Docker:
```bash
docker run --rm -v $(pwd):/github/workspace ghcr.io/atopile/atopile-kicad:latest
```

## Alternative Workflow
If the issue persists, consider using atopile directly in the workflow instead of the Docker image:

```yaml
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install atopile
  run: pip install atopile

- name: Build
  run: atopile build
```

## Reporting the Issue
If none of these solutions work, report the issue to:
- https://github.com/atopile/atopile/issues
- Include the full error message and your `ato.yaml` file