**KACO Blueplanet Hybrid 10.0 TL3 — Home Assistant Custom Integration**

Overview
- What: A Home Assistant custom integration to read data from KACO Blueplanet Hybrid 10.0 TL3 inverters (hy-sys).
- Goal: Provide native Home Assistant sensors (power, voltage, energy, battery, temperature). Optional MQTT publishing of the same values.

Prerequisites
- Firmware: The inverter must run firmware v8.
- hy-sys configuration (in the inverter / hy-sys software):
  - User Settings → Data Access → Enable Viewer Mode: ENABLED
  - User Settings → Data Access → Only from local network: DISABLED

Warning: Any firmware or configuration changes are performed at your own risk. See the Legal Disclaimer below.

Installation
- Copy the `kaco_inverter` folder to `<home_assistant_config>/custom_components/kaco_inverter/`.
- Restart Home Assistant.
- In Home Assistant: Settings → Devices & Services → Add Integration → search for "KACO Inverter" and follow the setup flow.

Configuration (Config Flow)
- Step 1 (required):
  - `inverter_host`: inverter IP address
  - `inverter_port`: inverter port (default: 9760)
  - `update_interval`: polling interval in seconds (default: 30, min: 5, max: 3600)
  - `mqtt_enabled`: enable MQTT publishing (default: false)
- Step 2 (only if MQTT enabled):
  - `mqtt_host`: MQTT broker hostname
  - `mqtt_port`: MQTT broker port (default: 1883)
  - `mqtt_username` / `mqtt_password`: optional credentials if your broker requires authentication

You can edit these settings later via Settings → Devices & Services → KACO Inverter → Configure. Fields are pre-filled with current values and a connection test is performed; saving will reload the integration automatically.

Available Home Assistant sensors
- Power (W): `Inverter Power L1/L2/L3`, `Inverter Power Total`, `Net Power Total`, `PV Power`, `Battery Power`, `Consumption Power Total`
- Voltage (V): `PV Voltage String 1/2`, `Battery Voltage`
- Battery: `Battery SOC (%)`, `Battery Cycles`
- Energy (kWh): `Grid Feed-in Today`, `Grid Consumption Today`, `Self Consumption Today`, `Battery Energy Today`, `Net Grid Consumption Today` and monthly equivalents
- Temperature: `Inverter Temperature`

The integration also computes several derived values (for example inverter total power, net total power, total consumption and net grid feed-in calculations).

Optional MQTT topics (when enabled)
Examples:
- `kaco/Power_Inv_L1`
- `kaco/Power_Inv_L2`
- `kaco/Power_Inv_L3`
- `kaco/Power_Inv_Total`
- `kaco/Power_Net_Total`
- `kaco/U_PV_1`, `kaco/U_PV_2`
- `kaco/P_PV`, `kaco/P_Bat`
- `kaco/SOC_Bat`
- `kaco/power_sum_cons`
- `kaco/today_grid_feed_in`, `kaco/this_month_grid_feed_in`
- `kaco/today_cons_from_grid`, `kaco/this_month_cons_from_grid`
- `kaco/today_cons_self`, `kaco/this_month_today_cons_self`
- `kaco/today_battery_energy_volume`, `kaco/this_month_battery_energy_volume`
- `kaco/real_grid_feed_in_today`, `kaco/real_grid_feed_in_month`
- `kaco/temp_inverter`

Technical notes
- The integration connects via TCP to the inverter (default port 9760), sends a brief authentication/handshake packet and then transmits several request packets to retrieve the required values.
- Default polling interval is 30 seconds. Short intervals increase CPU and network load.
- MQTT publishing uses `paho-mqtt` (declared as a dependency in `manifest.json`).

Troubleshooting
- Verify the hy-sys settings listed under Prerequisites.
- Test TCP connectivity from your Home Assistant host to the inverter (for example with `nc`, `telnet` or PowerShell `Test-NetConnection`).
- Check Home Assistant logs for connection errors or parser exceptions.

Legal disclaimer
- Use this integration at your own risk. The author is not responsible for any damage to the inverter, data loss, warranty voiding, or other consequences.
- Perform firmware or configuration changes only if you understand the risks.

Attribution
- This project is based on prior work by user "Ebsele" on the KNX-User-Forum. Original thread and relevant post:
  - https://knx-user-forum.de/forum/supportforen/smarthome-py/1954915-smarthome-ng-plugin-um-kaco-blueplanet-hybrid-10-0-tl3-auszulesen?p=1974754#post1974754

Contributing
- Pull requests are welcome — include tests and a short description.
- Open issues for bugs or feature requests.

Files in this package
- `kaco_inverter/__init__.py` — integration setup
- `kaco_inverter/manifest.json` — HA manifest (dependencies)
- `kaco_inverter/config_flow.py` — config & options flow
- `kaco_inverter/coordinator.py` — DataUpdateCoordinator (socket + MQTT)
- `kaco_inverter/parser.py` — hex parser
- `kaco_inverter/sensor.py` — sensor entities
- `kaco_inverter/strings.json` + `translations/` — UI texts

Support
- When opening an issue, include:
  - Home Assistant version
  - Inverter firmware version
  - Configuration details (do NOT include passwords)
  - Relevant debug log excerpts

Last updated: automatically generated README. Use at your own risk.


