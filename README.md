# MAC Address Changer
A Python3 utility to spoof MAC addresses on Linux. Includes features like random MAC generation, format validation, logging, and color-coded output for better UX.

---

## Features

- Change MAC address for any network interface
- Generate and apply a random valid MAC address (`--random`)
- Validate MAC address format before applying
- Logs all changes and failures to `mac_changer.log`
- Color-coded terminal output using `colorama`
- Requires **root** privileges for execution

---

## 📦 Requirements

- Python 3.x
- Kali Linux or any Linux with `ip` and `ifconfig`
- `colorama` Python module

### 📥 Installing Dependencies

Create a virtual environment (recommended):

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install colorama
```

Or install `colorama` via apt if available:

```bash
sudo apt install python3-colorama
```
---

## Usage

```bash
sudo python3 mac_changer.py -i <interface> -m <new-mac-address>
```

Example:

```bash
sudo python3 mac_changer.py -i wlan0 -m 00:11:22:33:44:55
```

Use random MAC:

```bash
sudo python3 mac_changer.py -i wlan0 --random
```

---

## Log File

All changes are logged to `mac_changer.log`:

```
[2025-05-23 14:52:10.123456] Changed wlan0 MAC from aa:bb:cc:dd:ee:ff to 02:4f:2a:9c:11:56
```

---

## Note

You **must run this script as root**:

```bash
sudo python3 mac_changer.py ...
```

---

## Disclaimer

Use responsibly. MAC spoofing can interfere with network operations and may violate policies on certain networks.



