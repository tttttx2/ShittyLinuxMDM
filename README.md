**Do not use this for productive systems!**


# ShittyLinuxMDM
This is a POC Linux MDM for educational purposes, which enables the simple deployment of configuration or compliance scripts. The web interface allows the management of those scripts and the reporting of the device status.

## Installation
Simply clone this repo and use `docker compose up -d` to get the MDM server running. The login credentials for the admin user can be set using the environment variable `ADMIN_PASS`.


# API Endpoints

## /api/device/create
Allows for the onboarding of new devices

## /api/device/edit
Allows for the enabling or disabling of specific scripts on this device. Disabling a script will not undo the actions executed by the script!

## /api/device/delete
Allows for the removal of a device. Future pulls from the device will fail with HTTP Status 404

## /api/device/list
Allows for the listing of device config and status. If the parameter `deviceid` is provided, only the status of the specific device is returned.

## /api/config/edit
Allows for the editing of the script
