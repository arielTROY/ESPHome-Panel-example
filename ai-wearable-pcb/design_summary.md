# AI Wearable PCB Design Summary

## Overview
This ultra-compact AI wearable PCB is designed to meet the following requirements:
- **Size**: < 30mm × 30mm (targeting 25mm × 28mm)
- **Functionality**: Camera capture, continuous audio recording, AI processing via cloud APIs
- **Power**: 8+ hour battery life with smart power management
- **Connectivity**: eSIM/LTE-M for global cellular connectivity
- **Development**: Arduino IDE compatible

## Component Selection Justification

### 1. Main Processor: nRF52840
- **Why**: Ultra-low power consumption (< 1mA in active mode)
- **Features**: 
  - ARM Cortex-M4F @ 64MHz
  - 1MB Flash, 256KB RAM
  - Built-in BLE 5.0 for optional smartphone connectivity
  - Arduino IDE support via Adafruit nRF52 core
  - USB support for programming
- **Power**: 4.8mA TX @ 0dBm, 4.6mA RX
- **JLCPCB Part**: C190794 (nRF52840-QIAA-R)

### 2. Camera: OV7675 or Alternative Ultra-Small Module
- **Why**: Smallest available camera sensor with acceptable quality
- **Features**:
  - VGA resolution (640×480)
  - Wide FOV lens
  - SPI interface for fast data transfer
  - Low power: ~15mA active
- **Size**: < 5mm × 5mm including lens

### 3. Microphone: ICS-41350
- **Why**: Ultra-small MEMS microphone with excellent power efficiency
- **Features**:
  - PDM digital output
  - 65dB SNR
  - Bottom port for better acoustic performance
  - Power: 650µA typical
- **Size**: 3mm × 4mm × 1mm

### 4. Speaker: 5mm Piezo + PAM8302A Amplifier
- **Why**: Smallest audio solution with acceptable quality
- **Features**:
  - Class-D efficiency > 85%
  - 2.5W output capability
  - Shutdown mode < 1µA
- **Total Size**: < 8mm × 8mm

### 5. Cellular Module: SIM7080G
- **Why**: Smallest LTE-M/NB-IoT module with integrated eSIM
- **Features**:
  - Global LTE-M/NB-IoT bands
  - Integrated eSIM
  - Low power: 1.4mA PSM, 9µA in sleep
  - AT command interface
- **Size**: 16mm × 16mm × 2.3mm

### 6. Power Management: BQ25125 PMIC
- **Why**: All-in-one solution for battery management
- **Features**:
  - Li-ion/Li-poly charger
  - Dual LDO outputs (3.3V, 1.8V)
  - Power path management
  - I²C control
- **Size**: 2.17mm × 2.33mm WCSP

### 7. Battery: 150-200mAh Li-poly
- **Why**: Best energy density for size
- **Features**:
  - Ultra-thin form factor (< 3mm thick)
  - Protection circuit included
  - Pico-blade connector

### 8. Charging: Magnetic Pads
- **Why**: Most space-efficient charging solution
- **Features**:
  - No connector wear
  - Waterproof potential
  - 2 pads + alignment magnets

## Power Budget Estimate

| Component | Active (mA) | Sleep (mA) | Duty Cycle | Average (mA) |
|-----------|------------|------------|------------|--------------|
| nRF52840  | 5.0        | 0.002      | 20%        | 1.00         |
| Camera    | 15.0       | 0.001      | 5% (3s/min)| 0.75         |
| Microphone| 0.65       | 0          | 100%       | 0.65         |
| Cellular  | 23.0       | 0.009      | 2%         | 0.47         |
| PMIC      | 0.5        | 0.5        | 100%       | 0.50         |
| **Total** |            |            |            | **3.37 mA**  |

**Battery Life**: 200mAh / 3.37mA = ~59 hours (2.5 days)
**With 8-hour target**: Can use 150mAh battery or increase functionality

## PCB Stack-up
- **Layers**: 4-layer PCB for better signal integrity and size optimization
- **Thickness**: 0.8mm
- **Material**: Standard FR-4
- **Minimum Via**: 0.2mm (8mil)
- **Minimum Trace**: 0.1mm (4mil)

## Size Optimization Strategies
1. **Component Placement**: All components on top side except test points
2. **Modular Design**: Camera and cellular antenna can extend slightly beyond main PCB
3. **0201 Passives**: Using smallest passive components where possible
4. **Integrated Antennas**: Chip antennas for both BLE and LTE

## Assembly Considerations
- **JLCPCB SMT**: All main components available
- **Special Requirements**: 
  - Camera module may need manual placement
  - Magnetic charging pads are through-hole

## Software Architecture
```cpp
// Arduino sketch structure
void setup() {
  // Initialize nRF52840 peripherals
  // Configure power management
  // Setup camera (SPI)
  // Setup microphone (PDM)
  // Setup cellular (UART AT commands)
}

void loop() {
  // Capture image every 20 seconds
  // Process audio continuously
  // Send data via cellular when buffer full
  // Enter low-power mode between operations
}
```

## Performance Assumptions
1. **Image Capture**: VGA JPEG ~50KB every 20 seconds
2. **Audio**: 8kHz mono compression to ~1KB/second
3. **Data Usage**: ~20MB/hour
4. **AI Processing**: Cloud-based (Gemini API or similar)
5. **Response Time**: 2-5 seconds for AI responses

## Future Improvements
1. Add accelerometer for motion-based wake
2. Implement edge AI for basic on-device processing
3. Add haptic feedback motor
4. Integrate flexible battery for wearable form factor
5. Add waterproofing with conformal coating

## BOM Cost Estimate (Volume 100+)
- nRF52840: $4.50
- Camera module: $3.00
- Cellular module: $12.00
- PMIC: $1.50
- Other components: $5.00
- PCB: $2.00
- **Total**: ~$28.00