# HA Mars Hydro

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Community Forum][forum-shield]][forum]

## Mars Hydro Cloud Integration
This integration communicates with the Mars Hydro Cloud and controls and monitors your Mars Hydro devices (lights and fans) through Home Assistant.

⚠️ Warning: API only supports one device to be logged in, so you will get kicked out of the app as soon as you login.

## Additional Note
Since I only own one device (an FC3000 Light), I initially focused on supporting that device. However, support for **fans** and their controls has now been added. If you have the Bluetooth Stick, this integration should work with your devices.

## Features Added:
- **Fan Entity**:
  - Control fan speed via a slider (25%-100%).
  - Monitor fan speed as a percentage.
- **Fan Sensors**:
  - **Temperature (°F and °C)**.
  - **Humidity**.
  - **Fan speed**.
- **Device Images**: (work in progress)
  - Device images are getting displayed in Home Assistant soon

## Background
- This integration is designed for **Mars Hydro FC...** lights and compatible fans running with the Bluetooth USB Stick.
- It allows you to:
  - Control light brightness and fan speed.
  - Control device power via a switch.
  - Monitor brightness, temperature, humidity, and fan speed.
- This integration is built for the Home Assistant platform to manage your Mars Hydro devices through the cloud API.

## Setup

### Installation:
* Go to HACS -> Integrations
* Click the three dots on the top right and select `Custom Repositories`
* Enter `https://github.com/suppqt/ha_mars_hydro` as the repository, select the category `Integration` and click Add.
* A new custom integration called **Mars Hydro** should now show up in your HACS. Install it.
* Restart Home Assistant.

### Configuration:
1. **Login and Connect Devices in the Mars Hydro App**:
   - Before using this integration, ensure you have logged into the **Mars Hydro app** and connected your devices.

2. **Login**:
   - The integration will require your **email** and **password** from the Mars Hydro app.

3. **Automatic Device Discovery**:
   - The integration will fetch device data and create entities for:
     - **Light brightness control**.
     - **Fan speed control**.
     - **Temperature (°F/°C)**.
     - **Humidity**.
     - **Fan speed sensor**.
     - **Switch control for lights and fans**.

### Entities Created:
- **Light Brightness Control**: Adjust brightness of your Mars Hydro light.
- **Fan Speed Control**: Adjust fan speed (slider, 25%-100%).
- **Temperature Sensors**: Displays fan temperature in °F and °C.
- **Humidity Sensor**: Displays fan humidity.
- **Fan Speed Sensor**: Displays fan speed percentage.
- **Switch Control**: Power on/off for lights and fans.

#### Notes:
- This integration uses the **Mars Hydro Cloud API**. Ensure your devices are connected to the cloud and reachable.
- You may need to create an account in the Mars Hydro app and provide your credentials to authenticate and link your device.

#### Disclaimer:
- This is my first custom component, and while I strive for quality, there may still be issues. Feedback and contributions are always appreciated!

## Contributions are welcome!

If you want to contribute to this integration, please read the [Contribution guidelines](CONTRIBUTING.md).

***

[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/suppqt/ha_mars_hydro.svg?style=for-the-badge
[commits]: https://github.com/suppqt/ha_mars_hydro/commits/main
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/suppqt/ha_mars_hydro.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%20%40suppqt-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/suppqt/ha_mars_hydro.svg?style=for-the-badge
[releases]: https://github.com/suppqt/ha_mars_hydro/releases
