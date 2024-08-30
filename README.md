# Disk Space Alert Script

This Python script monitors disk usage on a Linux system and sends an email alert if any partition exceeds a specified usage threshold. It is designed to run on systems with Python 3 installed.

## Prerequisites

  **Python 3**: The script will check if Python 3 is installed. If not, it attempts to install it using the system's package manager (`apt-get` or `yum`).

## Installation

Follow these steps to set up and use the disk space alert script:

1. **Clone the repository**:


   git clone <repository-url>
   cd <repository-directory>

2. **Make the script executable**:

    chmod +x disk_space_alert.py
   
3. **Run the script**:

     python3 disk_space_alert.py
