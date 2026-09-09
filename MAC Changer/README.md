# Linux MAC Address Changer Utility

A lightweight, automated Python utility designed for modifying the Media Access Control (MAC) address of network interfaces on Linux operating systems. Built with native Python modules, this script allows penetration testers, security researchers, and system administrators to quickly spoof network identifiers for privacy, testing, or security assessments.

---

## Key Features

* **Interface Management:** Automatically brings network interfaces down and up during the MAC address modification process using native `iproute2` commands (`ip link`).
* **Input Validation:** Employs Regular Expressions (Regex) to validate user-supplied MAC address formats before executing system-level modifications.
* **Safe Subprocess Execution:** Uses list-based command calls via Python's `subprocess` module to prevent Command Injection vulnerabilities.
* **Command-Line Interface:** Implements `argparse` for flexible flag-based usage in terminal environments and automated scripts.
* **Zero External Dependencies:** Built entirely with Python standard library modules (`subprocess`, `argparse`, `re`).

---

## Prerequisites & Requirements

* **Operating System:** Linux distributions (Ubuntu, Kali Linux, Debian, Arch, Fedora, etc.).
* **Privileges:** Root/Sudo access (required for modifying network interfaces).
* **Python Version:** Python 3.x

---

## Installation

Clone the repository to your local machine:

```bash
git clone [https://github.com/your-username/mac-address-changer.git](https://github.com/your-username/mac-address-changer.git)
cd mac-address-changer
