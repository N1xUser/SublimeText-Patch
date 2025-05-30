# 🖥️ ST-Patch

## 🌟 Overview

The **Sublime Text Patcher** is a powerful Python utility designed to patch the HEX values from 80 79 05 00 0F 94 C2 to C6 41 05 01 B2 00 90 and restore Sublime Text installation in case you want to go back. This script manage Sublime Text executable files and prevent unwanted updates if needed.

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Windows Support](https://img.shields.io/badge/Platform-Windows-informational.svg)

## ✨ Features

- 🔒 Patch Sublime Text executable
- 🔄 Restore Sublime Text to its original state
- 🚫 Block Sublime Text update servers via hosts file modification
- 💻 Supports multiple drive locations in case is not installed on the main disk
- 🛡️ Requires administrator privileges to work

## 🔧 Prerequisites

- Windows Operating System
- Python 3.8 or higher
- Administrator Privileges
- Installed Sublime Text Build 4180/4200 or older

## 📦 Required Dependencies

- `psutil`
- `shutil`
- `ctypes`

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/N1xUser/SublimeText-Patch.git
   cd SublimeText-Patch-main
   ```

2. Install required dependencies:
   ```bash
   pip install psutil
   ```

## 💡 Usage

### Running the Script

Run the script with administrator privileges:

```bash
SublimeTextPatch.py
```

### Interactive Menu Options

1. **Patch Sublime Text**
   - Creates a backup of the current executable with the .bkp extension
   - Modifies the executable to disable specific functionalities
   - Blocks update servers via hosts file

2. **Restore Sublime Text**
   - Restores the executable from the backup
   - Removes update server blocks from hosts file

## ⚠️ Important Warnings

- **Always backup your data before running the script**
- **Requires administrative permissions**

## 🛡️ Safety Measures

- Automatic backup creation before modifications
- User confirmation for critical actions
- Comprehensive error handling

## 🐛 Reporting Issues

Report any issues or suggest improvements by opening a GitHub issue in the repository.

---

### 🌈 Disclaimer

This script is provided "as is" without warranty of any kind. Use it responsibly and at your own discretion.

