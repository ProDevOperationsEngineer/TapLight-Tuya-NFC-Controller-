"""CSV database functionality"""
import csv
import os
from datetime import datetime

LOG_FILE = "history.csv"


def log_request(ip, command_path):
    """Logs NFc commands to the CSV database"""
    cleaned_command = command_path.lstrip('/').replace('_', ' ').title()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w', encoding='utf-8').close()

    with open(LOG_FILE, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, ip, cleaned_command])


def read_logs():
    """displays the entire CSV database"""
    with open(LOG_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        return sorted(rows, key=lambda row: row[0], reverse=True)
