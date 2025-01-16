# HA Mars Hydro

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Community Forum][forum-shield]][forum]

## Mars Hydro Cloud Integration
This integration communicates with the Mars Hydro Cloud and controls and monitors your Mars Hydro light devices through Home Assistant.

## Background
- This integration is designed for **Mars Hydro FC...** and other compatible models that are running with the Bluetooth USB Stick.
- It allows you to control the light's brightness, control the switch, and retrieve the brightness sensor value for your device.
- This integration is built to be used with the Home Assistant platform, providing an easy way to manage your Mars Hydro lights through the cloud API.

## Setup

### Installation:
* Go to HACS -> Integrations
* Click the three dots on the top right and select `Custom Repositories`
* Enter `https://github.com/suppqt/ha_mars_hydro` as the repository, select the category `Integration` and click Add.
* A new custom integration called **Mars Hydro** should now show up in your HACS. Install it.
* Restart Home Assistant.

### Configuration:
1. **Login to the Mars Hydro App**:
   * The integration will require your **email** and **password** from the Mars Hydro app to authenticate and link your account.
   
2. **Automatic Device Discovery**:
   * After logging in, the integration will automatically poll the Mars Hydro Cloud for your devices. It will fetch the necessary device data and create entities for:
     * **Brightness control**: Controls the brightness of your Mars Hydro light.
     * **Switch control**: Turns the device on/off.
     * **Brightness sensor**: Displays the current brightness level.

3. **Currently Supporting Only One Device**:
   * This integration currently supports **only one Mars Hydro device** (such as a light). Additional devices are not yet supported.
   * The integration is designed **specifically for light devices**. Other types of devices are not currently supported.

#### Entities Created:
- **Brightness Control**: Allows you to adjust the brightness of the connected Mars Hydro light.
- **Switch Control**: Turns the Mars Hydro light on or off.
- **Brightness Sensor**: Provides the current brightness level of the light (in percentage).

#### Notes:
- This integration uses the **Mars Hydro Cloud API** to interface with the lights. Ensure your devices are connected to the cloud and reachable.
- You may need to create an account in the Mars Hydro app and provide the app credentials (email/password) to authenticate and link your device.

#### Disclaimer:
- This is my first custom component, and I'm still learning to code in Python. While I strive to improve the code, there may be some areas that aren't fully optimized or could contain issues. Your understanding and any feedback are greatly appreciated as I continue to improve this integration!

## Contributions are welcome!

If you want to contribute to this integration, please read the [Contribution guidelines](CONTRIBUTING.md)

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
