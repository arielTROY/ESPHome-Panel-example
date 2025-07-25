# AI Wearable – 30 × 30 mm

This folder contains the entire Atopile source for an ultra-small AI wearable.  Running `ato build` will auto-generate KiCad schematic (`*.kicad_sch`), PCB (`*.kicad_pcb`), and project (`*.kicad_pro`) files plus a full machine-placeable BOM ready for JLCPCB.

## Key Components

| Function  | Part | Rationale | Typ. Current |
|-----------|------|-----------|--------------|
| MCU/AI    | **STM32U585QII** | Ultra-low-power Cortex-M33, DCMI, TrustZone, Arduino-core support | 38 µA/MHz run, 3 µA Stop2 |
| LTE Modem + eSIM | **nRF9160-SICA** | Cat-M1/NB-IoT, GPS, 2 µA PSM | 4 mA RRC-idle |
| Camera    | **OV2640 (105 ° lens)** | 2 MP, low-power standby, wide FoV | 20 mA active |
| Microphone| **ICS-41351 (PDM)** | Always-on digital mic | 0.65 mA |
| Speaker   | **MAX98357A + 15 mm exciter** | Class-D amp with tiny exciter | 3 mA idle |
| Charger   | **BQ25120A** | 28 µA quiescent LDO/charger | 28 µA |
| 3 V3 LDO  | **NCP161** | 25 µA quiescent | 25 µA |

### Power Budget (worst-case day-long average)

```
Camera:   20 mA × 1 s / 20 s  = 1.0 mA
Mic:                         0.65 mA
LTE (data bursts): 30 mA × 3 % = 0.9 mA
MCU:      active/standby mix   4.0 mA
Other:                        0.4 mA
-------------------------------------
Total ≈                        6.95 mA
```

With a 150 mAh Li-poly pouch cell this yields > 21 hours of runtime—comfortably exceeding the 8 h spec.

## Regenerating Outputs

```bash
pip install -U atopile   # one-time
ato build                # generate KiCad + BOM
```

All generated outputs land in `build/` and are automatically uploaded as artefacts by CI on every commit, following the pattern used in Atopile’s example GitHub projects.

License: CERN-OHL-S-2.0