These scripts are basic examples for tracking ArUco markers with the RealSense D435i on a Raspberry Pi 4 running Ubuntu 22.04.

## Prerequisites (single-time setup)
- Connect the Pi to WiFi
- Update all system programs with `sudo apt-get update && sudo apt-get upgrade`
- Install `openssh-server` with `sudo apt-get -y install openssh-server` on the Pi 4, assuming WiFi is already set up
- Install `v4l` utilities with `sudo apt-get -y install v4l-utils`, required to assign udev rules
- Install the RealSense SDK 2.0 on the Pi 4. Follow the instructions [here](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md), taking care not to install the kernel patches.
- Install opencv-contrib-python (includes additional libraries) with `pip3 install opencv-contrib-python`
- Extend the USBfs buffer size to 1000 MB:
    - Add `usbcore.usbfs_memory_mb=1000` to the `cmdline.txt` file in the `/boot/` directory (using sd card adapter)

## Execution (must be repeated each time)
- `ssh` into the Pi with the following argument:
    - `ssh -X pi@<ip_address>` (replace `<ip_address>` with the Pi's IP address)
- `cd` into the appropriate directory
- Set up the RealSense display with `export DISPLAY=:0`
- Run the script with `python3 mainIR_mult.py`

## Troubleshooting
- If the connection times out, unplug the RealSense camera, wait 3-5 seconds, and then replug
- The scripts will *likely* work if `rs-enumerate-devices` yields an immediate response
    - If `rs-enumerate-devices` hangs or takes more than a second to execute, unplug the camera and try again
