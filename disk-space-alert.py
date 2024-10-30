#!/usr/bin/env python3

import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Function to check if a command exists
def command_exists(command):
    return subprocess.call(f"type {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

# Function to install Python 3 based on the package manager
def install_python3():
    print("Python 3 is not installed. Installing Python 3...")
    if command_exists("apt-get"):
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3"], check=True)
    elif command_exists("yum"):
        subprocess.run(["sudo", "yum", "update", "-y"], check=True)
        subprocess.run(["sudo", "yum", "install", "-y", "python3"], check=True)
    else:
        print("Unsupported package manager. Please install Python 3 manually.")

# Step 1: Check if Python is installed
if not command_exists("python3"):
    install_python3()
else:
    print("Python 3 is already installed. Proceeding to the next step...")

# Step 2: Disk space alert script
# Threshold for disk space usage percentage
THRESHOLD = 5

# Email settings
TO_EMAIL = ["email@ankur.cloud", "email2@ankur.cloud", "email3@ankur.cloud"]
SUBJECT = f"Disk Space Alert on {os.uname().nodename}"
FROM_EMAIL = "disk@viitorcloud.co"

# SMTP server settings
SMTP_SERVER = "yoursmtphost"
SMTP_PORT = 587  # Common port for TLS
SMTP_USER = "yoursmtpuser"
SMTP_PASSWORD = "yoursmptpassword"

# Debugging Information
print("Starting disk check...")
print(f"Threshold: {THRESHOLD}%")

# HTML header for the email message
alert_message = """<html><body>
<h2>Disk Space Alert...</h2>
<table border='1' cellpadding='5' cellspacing='0'>
<tr><th>Partition</th><th>Total Space</th><th>Used Space</th><th>Available Space</th><th>Usage</th><th>Mounted On</th></tr>"""

# Flag to track if any partition exceeds the threshold
alert_flag = False

# Get disk usage for all partitions
df_output = subprocess.check_output("df -h", shell=True).decode()
lines = df_output.splitlines()

# Loop through each line (starting from the second line) to check usage
for line in lines[1:]:
    parts = line.split()
    filesystem = parts[0]
    total_space = parts[1]
    used_space = parts[2]
    available_space = parts[3]
    usage = int(parts[4].strip('%'))
    mounted_on = parts[5]

    if usage >= THRESHOLD:
        print(f"Partition {filesystem} mounted on {mounted_on} is over threshold with {usage}% used")
        alert_flag = True
        alert_message += f"<tr><td>{filesystem}</td><td>{total_space}</td><td>{used_space}</td><td>{available_space}</td><td>{usage}%</td><td>{mounted_on}</td></tr>"

# Close the HTML table
alert_message += "</table></body></html>"

# Send email if any partition exceeds the threshold
if alert_flag:
    print("Sending email alert...")
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = ", ".join(TO_EMAIL)
    msg['Subject'] = SUBJECT

    msg.attach(MIMEText(alert_message, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print("No partitions exceed the threshold.")
