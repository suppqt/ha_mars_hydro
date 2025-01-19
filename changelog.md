# Changelog

## Version 1.0.2

### 🚀 New Features

- **Fan Entity**
  - Added a fan entity with speed control via a slider (25%-100%).
  - Initial slider value uses `deviceLightRate` from `get_fandata`.
  - Included `async_turn_on`, `async_turn_off`, and detailed logging for improved control.

- **Fan Sensors**
  - Introduced new sensors to monitor:
    - **Temperature** (°F and °C).
    - **Humidity**.
    - **Fan speed**.
  - Handles invalid or missing data gracefully with enhanced logging.

### 🔧 API Updates

- Added a new `set_fanspeed` method, based on `set_brightness`, to control fan speed.
- Enhanced logging for all API calls, including detailed request and response data.

### 🖼️ Device Registry

- Integrated device images into Home Assistant using the `deviceImage` URL from `get_lightdata` and `get_fandata`.

### 🐛 Bug Fixes

- Fixed fan and light device ID mix-up issues.
- Ensured fan speed values are clamped to the valid range of 25%-100%.

### 📈 General Improvements

- Enhanced logging for debugging and monitoring.
- Improved dynamic handling of device names and IDs.
- Added robust error handling for a more seamless integration.

---

This release introduces fan support, expands sensor functionality, and significantly improves the integration's stability and usability.
