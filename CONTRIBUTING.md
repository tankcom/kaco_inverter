# Contributing to KACO Inverter

Thank you for your interest in contributing! This document provides guidelines for reporting issues and submitting improvements.

## Code of Conduct
- Be respectful and inclusive.
- No harassment, discrimination, or offensive language.

## Reporting Issues
Before opening an issue, please:
1. Check existing issues to avoid duplicates.
2. Test with the latest version of the integration.
3. Provide:
   - Home Assistant version
   - Inverter firmware version
   - Steps to reproduce
   - Relevant debug logs (with credentials and IPs redacted)

## Pull Requests

### Before you start
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Keep commits clean and descriptive.

### Code style
- Follow PEP 8.
- Use type hints where applicable.
- Keep functions small and focused.

### Testing
- Test your changes in a real Home Assistant instance or use the test files as a reference.
- Update documentation if behavior changes.

### Submitting a PR
1. Push to your fork.
2. Open a Pull Request with:
   - Clear description of what changed and why.
   - Link to related issue (if applicable).
   - Any new dependencies must be justified and added to `manifest.json`.
3. Wait for review and respond to feedback.

## Development Setup

```bash
git clone https://github.com/<yourusername>/kaco_inverter.git
cd kaco_inverter
# Create a test environment (optional):
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install paho-mqtt
```

## Questions?
Open a discussion or issue if you have questions before contributing.

Thank you for helping improve this integration!
