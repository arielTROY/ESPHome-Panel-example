# AI Wearable PCB - Atopile Design

## Overview

This project implements an ultra-compact AI wearable PCB designed using the [Atopile](https://atopile.io) framework. The design targets a 28mm × 28mm form factor with comprehensive AI capabilities including camera, microphone, speaker, and cellular connectivity.

## Features

- **ESP32-S3 Brain**: WiFi, BLE, camera interface, I2S audio
- **OV2640 Camera**: 2MP sensor with high FOV
- **SPH0645LM4H MEMS Microphone**: Always-on recording capability
- **MAX98357A Audio Amplifier**: Clear AI response playback
- **SIM7070G Cellular Module**: Global eSIM connectivity
- **BQ25185 + TPS63001 Power Management**: Efficient battery charging and regulation
- **500mAh LiPo Battery**: 28+ hour battery life
- **USB Type-C**: Charging and programming interface

## Project Structure

```
.
├── main.ato                    # Original full design
├── ai_wearable_final.ato      # Simplified version that builds successfully
├── power_management.ato        # Battery charging and power regulation
├── audio_system.ato           # Audio recording and playback
├── camera_interface.ato       # Camera module interface
├── cellular_module.ato        # eSIM cellular connectivity
├── esp32_s3.ato              # ESP32-S3 module definition
├── generics/                  # Generic component definitions
│   ├── resistors.ato
│   ├── capacitors.ato
│   └── inductors.ato
├── layouts/                   # Generated KiCad files
│   └── default/
│       ├── default.kicad_pcb
│       ├── default.kicad_pro
│       └── fp-lib-table
├── component-selection.md     # Detailed component analysis
├── project_summary.md         # Project overview and results
└── ato.yaml                  # Atopile project configuration
```

## Building the Project

### Prerequisites

1. Install Atopile:
```bash
pip install atopile
```

2. Install dependencies:
```bash
cd ai-wearable/my_first_ato_project
atopile install
```

### Build Commands

Build the PCB design:
```bash
python3 -m atopile build
```

This generates:
- KiCad PCB layout files in `layouts/default/`
- Bill of Materials in `build/builds/default/default.bom.csv`

## Design Specifications

- **PCB Size**: 28mm × 28mm (4-layer)
- **Power Consumption**: ~17.6mA average
- **Battery Life**: 28+ hours (500mAh battery)
- **Development**: Arduino IDE compatible (ESP32-S3)
- **Manufacturing**: JLCPCB ready with LCSC part numbers

## Key Components

| Component | Part Number | Description |
|-----------|-------------|-------------|
| ESP32-S3-WROOM-1 | C2913202 | Main processor |
| OV2640 | C2839795 | 2MP camera module |
| SPH0645LM4H | C2688116 | I2S MEMS microphone |
| MAX98357A | C2684264 | I2S audio amplifier |
| SIM7070G | C2830486 | Global cellular module |
| BQ25185 | C2837321 | Battery charger |
| TPS63001 | C88313 | Buck-boost converter |

## Next Steps

1. **PCB Layout**: Open `layouts/default/default.kicad_pcb` in KiCad
2. **Component Placement**: Optimize for 28mm × 28mm target
3. **Routing**: Complete 4-layer PCB routing
4. **Manufacturing**: Export Gerbers and order from JLCPCB

## Documentation

- [Component Selection Analysis](component-selection.md)
- [Project Summary](project_summary.md)
- [Atopile Documentation](https://docs.atopile.io)

## License

This project is open source. Feel free to use and modify for your own AI wearable designs.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
