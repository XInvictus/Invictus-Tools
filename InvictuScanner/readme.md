# Python Port Scanner

A simple port scanner written in Python that scans open ports on a target IP address. It uses `socket` to connect to each port and check if it's up.

## Features

- Scan a range of ports on a target IP
- Grab the banner or title of the target
- Display in a clean unicode table

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jwe0/invicscanner
    ```
2. Navigate into the project directory:
    ```bash
    cd port-scanner
    ```
3. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
4. Run the file
    ```bash
    python3 main.py
    ```
5. Input your target IP and port range