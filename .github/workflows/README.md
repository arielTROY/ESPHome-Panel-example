# GitHub Actions Workflows for AI Pin PCB Project

This directory contains GitHub Actions workflows for building, validating, and exporting PCB designs from atopile to KiCad format.

## Workflows Overview

### 1. `atopile-kicad-build.yml` - Main Build and Export Workflow
**Purpose**: Comprehensive workflow that builds atopile projects, validates PCB designs, and exports various formats.

**Features**:
- Builds multiple atopile projects in parallel
- Runs ERC (Electrical Rules Check) and DRC (Design Rules Check)
- Exports schematics (PDF, SVG)
- Exports PCB manufacturing files (Gerbers, drill files)
- Generates 3D models (STEP format)
- Creates interactive BOMs
- Packages files for JLCPCB manufacturing

**Triggers**: Push/PR to main branch, manual dispatch

### 2. `atopile-docker-build.yml` - Docker-based Build
**Purpose**: Uses the official atopile-kicad Docker image for consistent builds.

**Features**:
- Builds using the official atopile Docker container
- Processes all atopile projects automatically
- Exports all KiCad formats using kicad-cli
- Creates JLCPCB-ready packages
- Generates comprehensive documentation

**Triggers**: Push/PR to main branch, manual dispatch

### 3. `kibot-advanced-export.yml` - Advanced Manufacturing Outputs
**Purpose**: Uses KiBot for professional-grade PCB documentation and manufacturing files.

**Features**:
- High-quality PCB renders with PcbDraw
- 3D visualization
- Assembly documentation
- JLCPCB-specific outputs with proper formatting
- Manufacturing reports
- Batch processing of multiple boards

**Triggers**: Push to main branch, manual dispatch with optional project selection

### 4. `ai-wearable-build.yml` - Original Simple Build
**Purpose**: Basic atopile build workflow (kept for compatibility).

**Features**:
- Simple atopile build command
- Uploads build artifacts

## Usage

### Running Workflows Manually

All workflows support manual triggering via GitHub Actions tab:

1. Go to Actions tab in your repository
2. Select the workflow you want to run
3. Click "Run workflow"
4. Select branch and any inputs (if applicable)

### Workflow Outputs

All workflows generate artifacts that can be downloaded from the Actions tab:

- **Build Artifacts**: Raw atopile build outputs
- **KiCad Exports**: Processed PCB files in various formats
- **Manufacturing Files**: Ready-to-use files for PCB fabrication
- **Documentation**: PDFs, images, and interactive BOMs

## File Formats Generated

### Documentation
- **PDF**: Schematic diagrams
- **SVG**: Vector graphics of schematics
- **PNG**: PCB renders (top/bottom views)
- **HTML**: Interactive BOMs for assembly

### Manufacturing
- **Gerbers**: PCB layer files
- **Excellon**: Drill files
- **STEP**: 3D models
- **CSV**: Component positions and BOMs
- **ZIP**: JLCPCB-ready packages

### Validation
- **ERC Reports**: Electrical rule violations
- **DRC Reports**: Design rule violations

## Best Practices

1. **Always review ERC/DRC reports** before sending boards to manufacturing
2. **Use interactive BOMs** for assembly verification
3. **Check 3D models** to ensure component placement
4. **Verify Gerbers** with a viewer before ordering

## Troubleshooting

### Build Failures
- Check the atopile syntax in `.ato` files
- Ensure all dependencies are specified in `ato.yaml`
- Review error logs in the Actions tab

### Export Issues
- Verify KiCad files were generated successfully
- Check file paths and permissions
- Ensure Docker image is accessible (for Docker-based workflows)

### Missing Outputs
- Some exports may fail silently - check individual step logs
- Ensure the PCB design is complete (has edges, etc.)
- Verify component models are available for 3D export

## Contributing

When adding new workflows:
1. Follow the existing naming convention
2. Document the workflow purpose and features
3. Add appropriate triggers and inputs
4. Include error handling and status reporting
5. Update this README

## Related Documentation

- [Atopile Documentation](https://docs.atopile.io)
- [KiCad CLI Documentation](https://docs.kicad.org/master/en/cli/cli.html)
- [KiBot Documentation](https://github.com/INTI-CMNB/KiBot)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)