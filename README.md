# 💡 Smart Light Control with NFC and Flask (Deltaco SH-LE27RGB) 💡


TapLight is an NFC-based smart lighting controller that allows you to toggle and configure Tuya-powered lights using NFC tags and a local Flask server.
Built around the Deltaco SH-LE27RGB but adaptable to other Tuya-compatible devices.


![Communication Flow](static/images/intro.png)


Project Overview – NFC-Triggered Smart Light Control (Deltaco + Flask)

This project allows you to control a smart RGB light using NFC tags and Python, all running on a local Flask web server.
It’s designed to integrate smoothly with the Deltaco SH-LE27RGB smart bulb, using Tuya’s cloud platform behind the scenes.
Three key lighting modes are included by default:

    /on_off – toggles the light on or off

    /warm_light – sets a warm white brightness mode

    /rgb_light – activates a colorful, animated RGB scene


These modes reflect the lighting styles I personally found most enjoyable,
but the project is fully modular — you can easily adapt the code to control the light in any way you like:
custom colors, transitions, brightness levels, scenes, or even timed behavior.


## Tested Hardware – What This Works With

    ✅ Confirmed: Deltaco SH-LE27RGB (a Tuya-based RGB smart bulb)

    Should also work with: any smart light using the Tuya platform, as long as:

        It supports control via Tuya Cloud API

        You can retrieve its Device ID and Local Key via tinytuya


Deltaco smart home products don’t expose a public API themselves —
but they are Tuya-based, meaning their functionality can be accessed using the Tuya Cloud API.

Tuya powers hundreds of smart home brands (including Deltaco, Teckin, BlitzWolf, Gosund, and more),
so this project can be adapted to many similar lights, switches, and plugs.


## How to Set Up a Tuya Developer Account (step-by-step)


Setting up Tuya for the first time can be a bit overwhelming — here's how to do it:

    Create a Tuya Developer Account

        Go to: https://iot.tuya.com

        Sign up for a free account

        Log in and go to the Cloud → Development section

    
    Create a Cloud Project

        Click "Create Cloud Project"
        
        Name it anything 
        
        Choose "Smart Home" as the industry

        Select your region (make sure to pick the same one as your smart life app configuration has otherwise they won't be able to connect)

        Enable the following APIs:

            Device Management

            Device Control

            User Management

    
    Link Your Tuya App Account

        Download and open the Smart Life app on your phone

        Log in using the same email address you used for the developer portal

        In the Tuya developer portal, go to "Devices" → "Link Tuya App Account"

        Use the QR code scanner in the app to link your mobile account to your developer project

    
    Pair Your Smart Light to the App

        Use the Smart Life or Tuya Smart app to set up your Deltaco light as usual

        Confirm that it appears in the app and works manually

    
    Get Credentials

        From the Tuya Developer Console:

            Copy your API Key

            Copy your API Secret

            Get your Device ID (found under Devices)

        These values are used in your .env file in this project

## Installing Dependencies

This project relies on a few Python libraries for Flask routing, environment variable handling, and Tuya API integration.

To install the required packages, run:

pip install -r requirements.txt

This will install the following:

    flask – lightweight web framework used to create the local server

    python-dotenv – for securely loading API credentials from a .env file

    tinytuya – for controlling Tuya-based smart devices via the Tuya Cloud API

## Environment Variables

Before running the app, you need to create a `.env` file in the project root with the following content:

API_REGION=your-region-code 
API_KEY=your-tuya-api-key 
API_SECRET=your-tuya-api-secret 
API_DEVICE_ID=your-device-id

Replace `your-region-code`, `your-tuya-api-key`, `your-tuya-api-secret`, and `your-device-id` with your actual Tuya Cloud API details.

The project uses three NFC tags to control a smart light via HTTP requests.
Each tag is linked to a specific command served by the Flask backend.

Requires NFC Tags

You’ll need 3 NFC tags, each assigned to one of the following commands:
Tag Purpose	Flask Route	Example URL
Toggle on/off	       /on_off	http://<your-ip>:5000/on_off
Set warm white mode	/warm_light	http://<your-ip>:5000/warm_light
Set RGB scene mode	/rgb_light	http://<your-ip>:5000/rgb_light


## Step-by-Step Instructions (MacroDroid)

    Download MacroDroid

    Create a Macro for Each NFC Tag For each of the three tags:

        Tap ➕ to create a new macro

        Trigger → NFC Tag → Scan the tag

        Action → HTTP Request:

            Method: GET

            URL: http://<your-computer-ip>:5000/<route>

                Example: http://192.168.1.123:5000/on_off

            Leave headers/body empty

        Save and name the macro accordingly

    Test the Tags

        Ensure your Flask server is running:

        app.run(host="0.0.0.0", port=5000)

        Your phone and the computer must be on the same Wi-Fi network

        Scan the NFC tags and confirm that they trigger the correct light behavior

## Tip

The routes are defined in app.py, and you see all requests using the project’s built-in /history page to verify activity.




