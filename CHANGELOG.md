# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of KACO Inverter integration
- Native Home Assistant sensors for:
  - Power values (inverter, grid, PV, battery, consumption)
  - Voltage readings (PV strings, battery)
  - Battery state of charge and cycle count
  - Energy counters (grid feed-in, consumption, self-consumption, battery)
  - Inverter temperature
- Config flow with step-by-step setup
- Options flow for updating settings after installation
- Support for dynamic update intervals (5–3600 seconds)
- Optional MQTT publishing with backward-compatible topic names
- German and English UI translations
- Comprehensive README with prerequisites and troubleshooting

### Technical
- DataUpdateCoordinator-based polling architecture
- Hex packet parsing from inverter responses
- TCP socket communication with authentication handshake
- Proper Home Assistant entity naming and device info

## Prerequisites
- Inverter firmware v8
- hy-sys configuration with Viewer Mode enabled and "Only from local network" disabled

## Attribution
Based on prior work by user "Ebsele" on KNX-User-Forum.
