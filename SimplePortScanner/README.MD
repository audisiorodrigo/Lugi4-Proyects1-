# Multithreaded TCP Port Scanner & Banner Grabber

A lightweight, high-performance **TCP Port Scanner** written in Python 3. Built using concurrent threading (`concurrent.futures`) and native socket operations, this tool allows security enthusiasts, penetration testers, and network administrators to perform rapid port discovery, service identification, and basic banner grabbing without external dependencies.

---

## Key Features

* **High-Speed Multithreading:** Leverages Python's `ThreadPoolExecutor` to handle concurrent TCP socket connections, dramatically reducing scan duration compared to single-threaded alternatives.
* **Banner Grabbing:** Automatically attempts to retrieve service banners upon identifying open TCP ports to aid in service version enumeration.
* **Flexible Input Parsing:** Supports continuous port ranges (e.g., `1-1024`) and specific comma-separated lists (e.g., `80,443,8080`).
* **Command-Line Interface:** Designed with `argparse` for seamless integration into terminal environments and automated bash pipelines.
* **Zero External Dependencies:** Relies entirely on Python standard library modules (`socket`, `argparse`, `datetime`, `concurrent.futures`).

---

## Installation

No external package installation (via `pip`) is required. Simply clone the repository using Git:

```bash
git clone [https://github.com/your-username/multithreaded-port-scanner.git](https://github.com/your-username/multithreaded-port-scanner.git)
cd multithreaded-port-scanner
