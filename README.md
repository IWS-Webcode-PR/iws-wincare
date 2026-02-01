# IWS-WinCare

Professional Windows 10/11 repair and system maintenance toolkit built with Python and PySide6.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)

---

**Developed by [IWS-Webcode.eu](https://iws-webcode.eu)**

---

## Overview

IWS-WinCare provides a modern, user-friendly interface for diagnosing and repairing common Windows issues. All operations are executed safely with proper error handling and logging.

## Features

### Bug-Fix Modules
- **DNS Cache Flush** - Clear DNS resolver cache
- **Winsock Reset** - Reset Windows Sockets catalog
- **Network Adapter Restart** - Restart network adapters
- **Windows Update Cache Repair** - Clear update cache
- **Explorer Cache Reset** - Clear icon and thumbnail cache
- **Temporary Files Cleanup** - Remove temp files
- **Environment Variables Refresh** - Broadcast environment changes

### Reset Modules
- **Network Reset** - Full network stack reset (IP, Winsock, Firewall)
- **Power Plan Reset** - Restore default power schemes
- **Default App Associations Reset** - Reset file associations
- **Windows Search Index Rebuild** - Rebuild search index
- **Start Menu Reset** - Fix Start Menu and Explorer issues
- **Windows Update Reset** - Soft-reset Windows Update components

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or higher
- Administrator privileges (required for system operations)

## Installation

```bash
git clone https://github.com/IWS-Webcode-PR/iws-wincare.git
cd iws-wincare
pip install -r requirements.txt
```

## Usage

```bash
python run.py
```

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name IWS-WinCare --icon=assets/icon.ico run.py
```

## Project Structure

```
iws-wincare/
├── src/
│   ├── app.py              # Application entry point
│   ├── ui/                 # User interface components
│   ├── core/               # Core execution logic
│   ├── modules/            # Repair and reset modules
│   ├── system/             # System-level operations
│   └── utils/              # Utilities and helpers
├── assets/                 # Application assets
├── logs/                   # Application logs
├── tests/                  # Unit tests
├── requirements.txt
├── pyproject.toml
└── run.py                  # Main entry point
```

## Security

- Administrator privileges required for most operations
- All critical actions require user confirmation
- No telemetry or external data transmission
- All operations logged locally

## Disclaimer

Use at your own risk. Create a system restore point before running repair operations. The authors are not responsible for any damage caused by this software.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

---

Copyright (c) 2024-2026 IWS-Webcode.eu
