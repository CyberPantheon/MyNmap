

# MyNmap: An Interactive Nmap Automation Tool

![Nmap Logo](https://nmap.org/images/sitelogo-nmap.svg)  
*MyNmap is a Python-based interactive tool that simplifies Nmap scans with a user-friendly menu-driven interface. It supports real-time output, advanced scan options, and beautiful formatting.*

---

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Examples](#examples)
5. [Contributing](#contributing)
6. [License](#license)

---

## Features ✨
- **Interactive Menu System**: Choose from a variety of Nmap scan types with ease.
- **Real-Time Output**: See scan results as they happen, with color-coded formatting.
- **Advanced Options**:
  - Timing and aggressiveness control (`-T0` to `-T5`).
  - Firewall/IDS evasion techniques.
  - Script scanning with NSE (Nmap Scripting Engine).
- **Output Formats**: Save results in normal, XML, grepable, or all formats.
- **Quick Scans**: Predefined scan presets for common tasks.
- **PDF Reporting**: Generate PDF reports from scan results.
- **Cross-Platform**: Works on Linux, macOS, and Windows (with Python installed).

---

## Installation 🛠️

### Prerequisites
- **Python 3.6+**: [Download Python](https://www.python.org/downloads/)
- **Nmap**: [Install Nmap](https://nmap.org/download.html)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MyNmap.git
   cd MyNmap
   ```

2. Install dependencies:
   ```bash
   pip install colorama fpdf
   ```

3. Run the script:
   ```bash
   python MyNmap.py
   ```

---

## Usage 🚀

### Running the Tool
1. Launch the script:
   ```bash
   python MyNmap.py
   ```

2. Follow the interactive menu to select scan types and options.

### Main Menu Options
- **Host Discovery**: Discover live hosts on a network.
- **Port Scanning**: Scan for open ports on a target.
- **Service/Version Detection**: Detect services and their versions.
- **OS Detection**: Guess the operating system of the target.
- **Script Scanning**: Run NSE scripts for advanced detection.
- **Firewall/IDS Evasion**: Use techniques to evade firewalls and IDS.
- **Traceroute**: Perform a traceroute to the target.
- **Aggressive Scan**: Enable aggressive scanning mode.
- **Custom Scan**: Enter custom Nmap flags.
- **Quick Scans**: Use predefined scan presets.

### Example Workflow
1. Choose **Port Scanning** from the main menu.
2. Select **TCP SYN Scan**.
3. Set timing to **Aggressive (-T4)**.
4. Save output to **XML format**.
5. Enter the target (e.g., `192.168.1.1/24`).
6. View real-time scan results.

---

## Examples 📖

### Quick Network Survey
```bash
python MyNmap.py
```
- Choose **Quick Scans** → **Network Survey**.
- Enter target: `192.168.1.0/24`.
- Results are displayed in real-time.


python MyNmap.py
```
- Choose **Quick Scans** → **Full Audit**.
- Enter target: `example.com`.
- Save output to **PDF format**.
- View the generated `report.pdf`.

---

## Contributing 🤝
Contributions are welcome! Here’s how you can help:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

---


---

## Acknowledgments 🙏
- **Nmap**: For providing an incredible network scanning tool.
- **Colorama**: For making terminal output beautiful.

---


---

## Support 💬
For questions or issues, please [open an issue](https://github.com/CyberPantheon/MyNmap/issues) on GitHub.

---

Enjoy using **MyNmap**! Happy scanning! 🚀

---


