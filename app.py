"""Main app, receives and handles data from NFT tags"""
import os
import sys
import tinytuya
from dotenv import load_dotenv
from flask import Flask, render_template, request
from logs import log_request, read_logs

# Setup connection to Tuya Cloud

load_dotenv()  # Load values from .env into environment variables

required_env_vars = ["API_REGION", "API_KEY", "API_SECRET", "API_DEVICE_ID"]

missing_vars = [var for var in required_env_vars if os.getenv(var) is None]

if missing_vars:
    print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
    print("Please create a .env file with your Tuya API credentials.")
    sys.exit(1)

cloud = tinytuya.Cloud(
    apiRegion=os.getenv("API_REGION"),
    apiKey=os.getenv("API_KEY"),
    apiSecret=os.getenv("API_SECRET"),
    apiDeviceID=os.getenv("API_DEVICE_ID")
)

DEVICE_ID = os.getenv("API_DEVICE_ID")
LOG_FILE = "history.csv"


app = Flask(__name__)


@app.route('/')
def home():
    """Main page"""
    return render_template('index.html')


@app.route('/delete_history', methods=['POST'])
def delete_history():
    """Deletes all data in CSV database"""
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w', encoding='utf-8').close()  # simply empty the file
    return render_template('history.html')


@app.route('/history')
def history():
    """Displays every NFC activated command sent to the server"""
    logs = read_logs()
    return render_template('history.html', logs=logs)


@app.route('/on_off')
def on_off():
    """On/off function"""
    ip = request.remote_addr
    status_response = cloud.getstatus(DEVICE_ID)
    # Extract current state
    try:
        status_items = status_response['result']
        switch_item = next(
            item for item in status_items
            if item['code'] == 'switch_led'
        )
        is_on = switch_item['value']
    except (KeyError, StopIteration):
        is_on = False
    # Toggle light
    new_state = not is_on
    command = {
        "commands": [{"code": "switch_led", "value": new_state}]
    }
    cloud.sendcommand(DEVICE_ID, command)
    log_request(ip, "On" if new_state else "Off")
    return render_template('index.html')


@app.route('/warm_light')
def warm_light():
    """Warm light function"""

    try:

        commands = [
            {"code": "work_mode", "value": "white"},
            {"code": "bright_value_v2", "value": 1000},
            {"code": "temp_value_v2", "value": 0}
        ]

        cloud.sendcommand(DEVICE_ID, {"commands": commands})

    except (KeyError, IndexError, TypeError) as e:
        print("Error accessing response data:", e)
    log_request(request.remote_addr, request.path)
    return render_template('index.html')


@app.route('/rgb_light')
def rgb_light():
    """switching between colours smoothly"""
    try:

        commands = [
            {"code": "work_mode", "value": "scene"}
        ]
        cloud.sendcommand(DEVICE_ID, {"commands": commands})
        log_request(request.remote_addr, request.path)

    except (KeyError, IndexError, TypeError) as e:
        print("Error accessing response data:", e)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
