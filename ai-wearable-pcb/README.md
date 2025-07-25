# AI Wearable Dev Board (30mm × 30mm)

This is an ultra-compact AI wearable development board designed for smart glasses, body cameras, and other wearable AI applications.

## Features

### Main Components

1. **MCU**: ESP32-S3-MINI-1 (LCSC: C2980299)
   - Dual-core Xtensa LX7 @ 240MHz
   - Wi-Fi 802.11 b/g/n
   - Bluetooth 5.0 (LE)
   - Camera interface support
   - AI acceleration capabilities

2. **Cellular Module**: SIM7080G (LCSC: C2943992)
   - LTE Cat-M1/NB-IoT
   - eSIM support via Nano SIM holder
   - Global band support
   - Low power consumption

3. **Camera**: OV2640
   - 2MP resolution
   - Wide FOV lens
   - Privacy LED indicator (red)
   - I2C control interface

4. **Audio**:
   - PDM Digital MEMS Microphone
   - MAX98357A I2S Audio Amplifier
   - 8Ω Speaker support
   - Recording LED indicator (orange)

5. **Power Management**:
   - USB-C connector with proper CC resistors (5.1kΩ)
   - BQ24074 LiPo battery charger (or similar)
   - TPS62840 ultra-low Iq buck regulator (3.3V)
   - BQ27441 fuel gauge
   - 400-600mAh LiPo battery support
   - NTC thermistor for battery temperature monitoring

6. **User Interface**:
   - Large "Query" button (6×6mm)
   - Reset button (3×3mm)
   - Boot button (3×3mm)
   - Slide power switch
   - Status LEDs:
     - Red: 5V USB power present
     - Green: 3.3V rail active
     - Blue: GPIO-controlled status
     - Orange: Recording active
     - Red: Camera privacy indicator

7. **Connectivity**:
   - USB-C for charging and data
   - QWIIC/I2C connector (JST-SH 4-pin)
   - Chip antenna for cellular

## Board Specifications

- **Size**: 30mm × 30mm (4-layer PCB recommended)
- **Component Size**: 0603 for all passive components
- **Power Input**: 5V via USB-C
- **Battery Voltage**: 3.7V nominal (LiPo)
- **System Voltage**: 3.3V
- **Current Consumption**: 
  - Sleep: <1mA
  - Active: ~200-500mA (depending on cellular/camera usage)

## Pin Connections

### ESP32-S3 Key Connections:
- **USB**: D+ and D- connected to USB-C with proper routing
- **Camera**: DVP interface (8-bit data + control signals)
- **Audio**: I2S interface to MAX98357A
- **Microphone**: PDM interface
- **Cellular**: UART interface to SIM7080G
- **I2C**: Shared bus for camera control, fuel gauge, and QWIIC connector
- **GPIO**: Status LEDs, button inputs, enable signals

### Protection Features:
- ESD protection on USB data lines
- RC circuits on MCU EN/RESET pins
- Proper bypass capacitors on all power rails
- Pull-up resistors on I2C bus (4.7kΩ)

## Assembly Notes

1. Place all 0603 components first
2. Ensure proper orientation of polarized components (LEDs, capacitors)
3. USB-C connector requires careful soldering
4. Battery should be mounted on the back of the PCB
5. Speaker can be connected via wire leads or pogo pins

## Software Support

The board is compatible with:
- Arduino IDE (ESP32 board package)
- ESP-IDF
- MicroPython
- CircuitPython

## Safety Considerations

- Battery charging is temperature monitored via NTC
- Overcurrent protection in charger IC
- Thermal regulation in buck converter
- Short-circuit protection on all outputs

## Applications

- Smart glasses
- Body cameras
- Health monitoring devices
- Asset tracking
- Environmental sensing
- AI-powered wearables
- Solar-powered devices (with appropriate input protection)

## LCSC Part Numbers Summary

- ESP32-S3-MINI-1: C2980299
- SIM7080G: C2943992
- BQ27441 (Fuel Gauge): C139621
- Nano SIM Holder: C2895022
- 0603 Resistors: Various values
- 0603 Capacitors: Various values
- LEDs (0603): Red, Green, Blue, Orange

## Design Files

- `main.ato`: Atopile hardware description
- `ato.yaml`: Project configuration
- Build outputs in `build/` directory

## Building

To build the project:
```bash
python3 -m atopile build
```

## License

This project is open source hardware. Feel free to modify and use for your projects.