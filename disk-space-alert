#!/usr/bin/env python3

import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Function to check if a command exists
def command_exists(command):
    return subprocess.call(f"type {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

# Step 1: Check if Python is installed
if not command_exists("python3"):
    print("Python3 is not installed. Installing Python 3...")
    subprocess.run(["sudo", "yum", "update", "-y"], check=True)
    subprocess.run(["sudo", "yum", "install", "-y", "python3"], check=True)
else:
    print("Python3 is already installed. Proceeding to the next step...")

# Step 2: Disk space alert script
# Threshold for disk space usage percentage
THRESHOLD = 5

# Email settings
TO_EMAIL = "hello@xyz.domain"
SUBJECT = f"Disk Space Alert on {os.uname().nodename}"
FROM_EMAIL = "disk@xyz.domain"

# SMTP server settings
SMTP_SERVER = "smtp_host"
SMTP_PORT = 587  # Common port for TLS
SMTP_USER = "smtp_user"
SMTP_PASSWORD = "smtp_password"

# Debugging Information
print("Starting disk check...")
print(f"Threshold: {THRESHOLD}%")
print("Checking disk usage on partition mounted on /...")

# HTML header for the email message
alert_message = """<html><body>
<h2>Disk Space Alert...</h2>
<table border='1' cellpadding='5' cellspacing='0'>
<tr><th>Partition</th><th>Total Space</th><th>Used Space</th><th>Available Space</th><th>Usage</th></tr>"""

# Flag to track if partition exceeds the threshold
alert_flag = False

# Get disk usage for the partition mounted on /
df_output = subprocess.check_output("df -h /", shell=True).decode()
lines = df_output.splitlines()
line = lines[1].split()
usage = int(line[4].strip('%'))
total_space = line[1]
used_space = line[2]
available_space = line[3]
partition = line[0]

if usage >= THRESHOLD:
    print(f"Partition {partition} is over threshold with {usage}% used")
    alert_flag = True
    alert_message += f"<tr><td>{partition}</td><td>{total_space}</td><td>{used_space}</td><td>{available_space}</td><td>{usage}%</td></tr>"

# Close the HTML table
alert_message += "</table></body></html>"

# Send email if threshold is exceeded
if alert_flag:
    print("Sending email alert...")
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
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
