# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this integration, please report it responsibly by emailing the maintainer directly. **Do not open a public GitHub issue** for security vulnerabilities.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Considerations

### For Users
- **Never hardcode credentials** in your Home Assistant configuration. Always use the config flow to provide MQTT credentials.
- **HTTPS for MQTT** is recommended if your broker supports it.
- **Local network only**: The integration communicates with your inverter over a TCP socket on the local network. Ensure the inverter is not exposed to the internet.
- **Firmware updates**: Keep your inverter firmware up to date.

### For Developers
- This integration handles inverter data over local TCP and optionally publishes to MQTT.
- MQTT credentials are stored in Home Assistant's secure configuration store (not in plaintext).
- No authentication is currently required to connect to the inverter itself — ensure your local network is properly secured.

## Known Limitations
- The integration relies on the inverter's TCP interface being available on the local network.
- Inverter firmware v8 is required; compatibility with other versions is untested.
- MQTT Export only works if a single Inverter is configured, otherwise the MQTT Values are mixed from all configured Inverters. If you need MQTT with multiple            configured Inverteres use Home Assistant Automations for MQTT export instead.

## Reporting Other Issues
For bug reports or feature requests (non-security), please open a GitHub issue with:
- Home Assistant version
- Inverter firmware version
- Reproduction steps
- Debug logs (with passwords/IPs redacted)
