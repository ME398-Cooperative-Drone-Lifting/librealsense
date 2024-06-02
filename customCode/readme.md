# To operate the RealSense camera in this framework:
## Prerequisites (single-time setup) [estimated time: 1-1.5 hours]
- Install Ubuntu 22.04 on a Raspberry Pi 4B (we have 8 GB RAM, your mileage may vary with less)
- Connect the Pi to WiFi
- Update all system programs with `sudo apt-get update && sudo apt-get upgrade`
- Install Python's `pip` module with `sudo apt-get install -y python3-pip`
- Install Python 3.7 with the following steps:
    - `sudo add-apt-repository ppa:deadsnakes/ppa`
    - `sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1`
- Install `openssh-server` with `sudo apt-get -y install openssh-server` on the Pi 4
    - Once the SSH server is set up, check the IP address in Settings/WiFi and write it down for recurring use in the execution section
- Install `video4linux` drivers with `sudo apt-get -y install v4l-utils`, required to assign udev rules
- Install the RealSense SDK 2.0 on the Pi 4. Follow the instructions [here](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md), taking care not to install the kernel patches.
- Install opencv-contrib-python (includes additional libraries) with `pip3 install opencv-contrib-python`
- Install the Python RealSense bindings with `pip3 install pyrealsense2`
- Extend the USBfs buffer size to 2048 MB:
    - Add `usbcore.usbfs_memory_mb=2048` to the `cmdline.txt` file in the `/boot/` directory (using sd card adapter)

## Execution (must be repeated each time)
- `ssh` into the Pi with the following argument:
    - `ssh -X pi@<ip_address>` (replace `<ip_address>` with the Pi's IP address)
- `cd` into `librealsense/customCode/arucoTracking/`
- Set up the RealSense display with `export DISPLAY=:0`
- Run `rs-enumerate-devices` to prime the RealSense USB buffer (mysterious, please do not ask why this works)
- Run the DroneKit code OR directly run the RealSense script with `python3 arucoTrack.py`
- If necessary, close the script with CTRL+C
- If you want to run either script again, you *must* run `rs-enumerate-devices` again before execution!

## Troubleshooting
- If the connection times out, unplug the RealSense camera, wait 3-5 seconds, and then replug in the other USB 3.0 port
- The scripts will *likely* work if `rs-enumerate-devices` yields an immediate response
    - If `rs-enumerate-devices` hangs or takes more than 2 seconds to execute, unplug the camera and try again
