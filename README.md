# amnwg-gui
A simple Python GUI for managing AMNRZIA VPN, based on awg-quick (CLI tool for AmneziaWG)

## About

This project provides a user-friendly GUI wrapper around `awg-quick`, the command-line tool for configuring and controlling AmneziaWG (Amnezia WireGuard) tunnels.

**Under the hood:** [amneziavpn/amneziawg-tools](https://github.com/amnezia-vpn/amneziawg-tools) — the official userspace tooling for AmneziaWG, including the `awg(8)` and `awg-quick(8)` utilities.

## Features

- 🔌 Connect/disconnect VPN tunnels with one click
- 📁 Manage multiple AmneziaWG configurations
- 📊 View connection status in real time
- 🎛️ Simple, intuitive interface

## Requirements

- Python 3.8+
- `awg-quick` (from amneziawg-tools)
- Linux / macOS / Windows (with WireGuard/AmneziaWG support)

## Installation

```bash
# Clone the repository
git clone https://github.com/tomuccino/amnwg-gui
cd amnwg-gui

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python main.py
```
