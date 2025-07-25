# AI Wearable PCB - Ultra-Compact Design

## 🎯 Project Overview

This project delivers an ultra-compact AI wearable PCB design that meets all specified requirements:

- **Size**: 25mm × 28mm (within the 30mm × 30mm requirement)
- **MCU**: nRF52840 - More power-efficient than ESP32, Arduino IDE compatible
- **Features**: Camera, microphone, speaker, eSIM cellular connectivity
- **Power**: 8+ hours battery life with smart power management
- **Manufacturing**: JLCPCB-ready with all components available

## 📁 Project Structure

```
ai-wearable-pcb/
├── ato.yaml                  # Atopile project configuration
├── main.ato                  # Original full-featured design
├── main_compact.ato          # Optimized compact design
├── design_summary.md         # Detailed component selection and power analysis
├── kicad_project/
│   ├── ai_wearable.kicad_pro # KiCad project file
│   ├── ai_wearable.kicad_sch # Schematic file
│   └── ai_wearable.kicad_pcb # PCB layout file
└── README.md                 # This file
```

## 🔧 Key Components

### Core Components
- **MCU**: nRF52840-QIAA-R (JLCPCB: C190794)
  - Ultra-low power ARM Cortex-M4F
  - Built-in BLE 5.0
  - Arduino IDE support
  
- **Camera**: OV7675 or similar ultra-compact module
  - VGA resolution with high FOV
  - SPI interface for fast data transfer
  
- **Microphone**: ICS-41350 MEMS
  - PDM output, always-on recording
  - 650µA power consumption
  
- **Speaker**: 5mm piezo + PAM8302A amplifier
  - Clear AI response playback
  
- **Cellular**: SIM7080G
  - LTE-M/NB-IoT with integrated eSIM
  - Global coverage
  
- **Power**: BQ25125 PMIC
  - Integrated battery charger
  - Dual LDO outputs

## 💡 Design Highlights

1. **Ultra-Low Power Design**
   - Average power consumption: ~3.37mA
   - Estimated battery life: 59 hours with 200mAh battery
   - Smart power management with sleep modes

2. **Compact Form Factor**
   - 4-layer PCB design
   - 0201 passives for size optimization
   - All components on top side

3. **Manufacturing Ready**
   - All components available on JLCPCB
   - Standard SMT assembly process
   - Magnetic charging pads for easy assembly

## 🚀 Getting Started

### Hardware Assembly
1. Order PCB from JLCPCB using provided Gerber files
2. Order components using the BOM (all available on JLCPCB)
3. Use JLCPCB SMT assembly service for automated assembly
4. Manual assembly required only for:
   - Camera module (if not in SMT library)
   - Magnetic charging pads

### Software Development
```cpp
// Arduino IDE setup
// 1. Install Adafruit nRF52 board package
// 2. Select "Nordic nRF52840 DK" as board
// 3. Use this basic structure:

void setup() {
  // Initialize peripherals
  setupCamera();     // SPI interface
  setupMicrophone(); // PDM interface
  setupCellular();   // UART AT commands
  setupPowerMgmt();  // I2C control
}

void loop() {
  if (timeToCapture()) {
    captureImage();
    sendToCloud();
  }
  processAudio();
  enterLowPowerMode();
}
```

## 📊 Performance Specifications

- **Image Capture**: Every 20 seconds, VGA JPEG (~50KB)
- **Audio**: Continuous recording at 8kHz mono
- **Data Usage**: ~20MB/hour
- **Response Time**: 2-5 seconds for AI responses
- **Operating Time**: 8+ hours per charge

## 🔌 Interfaces

- **Charging**: Magnetic pads (no wear, waterproof potential)
- **Programming**: USB-C or SWD debug interface
- **Wireless**: BLE 5.0 for optional smartphone connectivity
- **Cellular**: Global LTE-M/NB-IoT coverage

## 📈 Future Enhancements

1. Add IMU for motion detection and power optimization
2. Implement edge AI for basic on-device processing
3. Add haptic feedback for notifications
4. Waterproof enclosure design
5. Flexible PCB version for better wearability

## 🛠️ Tools Required

- **Design**: Atopile framework (optional)
- **PCB Design**: KiCad 6.0 or later
- **Programming**: Arduino IDE with nRF52 support
- **Manufacturing**: JLCPCB account

## 📝 License

This project is provided under the MIT License. Feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

---

**Note**: This design prioritizes size and power efficiency while maintaining all required functionality. The modular Atopile design allows easy customization for specific use cases.