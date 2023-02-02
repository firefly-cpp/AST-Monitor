## Basic AST-Monitor components
### Adafruit Ultimate GPS HAT for Raspberry Pi
Please follow the tutorial: [LINK](https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi)

### USB ANT+ stick
We used the SUUNTU MOVESTICK MINI stick, which did not require any specific hardware configuration.
You can use the following stick with the openant python library: [LINK](https://github.com/Tigge/openant)

### A five-inch LCD touch screen display
Please follow the following tutorial for touch calibration instructions: [LINK](https://www.waveshare.com/wiki/5inch_HDMI_LCD)


## Configuration of AST-Monitor
### Installation of Raspberry Pi OS
An SD card with the minimum capacity of 8 GB is required for the operating system. Before configuring the device itself, you must install Raspberry Pi OS to the SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/). As AST-Monitor apart from the touch screen cannot interact with a user, you must enable SSH and input the Wi-Fi SSID and password in Raspberry Pi Imager settings in order to enable remote access to the device.

### Remote access to AST-Monitor
When the installation of Raspberry Pi OS is sucessfully finished, you must insert the SD card to Raspberry Pi and plug AST-Monitor into a power source. After the boot of the device, you must connect to AST-Monitor using SSH protocol (open-source client [PuTTY](https://www.putty.org/) is recommended on Windows). It is crucial that both AST-Monitor and the device that runs an SSH client are connected to the same Wi-Fi network.

### Calibration of the touch screen
To enable the touch screen, you have to add the following lines in <i>/boot/config.txt</i>:
```
hdmi_group=2
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0
hdmi_drive=1
dtoverlay=ads7846,cs=1,penirq=25,penirq_pull=2,speed=50000,
          keep_vref_on=0,swapxy=0,pmax=255,xohms=150,xmin=200,
          xmax=3900,ymin=200,ymax=3900
display_rotate=3
```

Before calibrating the touch screen, additional packages are required. We can obtain and configure them by executing the following two commands:
```sh
$ sudo apt-get install xserver-xorg-input-evdev xinput-calibrator
$ sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf/usr/share/X11/xorg.conf.d/45-evdev.conf
```

In the next step, we have to create a file, named <i>99-calibration.conf</i> in the directory <i>/usr/share/X11/xorg.conf.d/</i> and paste the following lines into the newly created file:
```
Section "InputClass"
        Identifier      "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "Calibration"   "139 3891 4 3809"
        Option  "SwapAxes"      "1"
        Option "EmulateThirdButton" "1"
        Option "EmulateThirdButtonTimeout" "1000"
        Option "EmulateThirdButtonMoveThreshold" "300"
EndSection
```
Note: if a touch screen is still not calibrated correctly, please follow calibration instructions: [LINK](https://www.waveshare.com/wiki/5inch_HDMI_LCD).

The touch screen is initially rotated by 180 degrees. To rotate the screen, you have to truncate <i>/etc/xdg/-lxsession/LXDE-pi/autostart</i> file. After doing that, you have to add the following two lines to the file:
```
@xrandr -o 2
@xcompmgr -C -c -o 0.5 -l -19 -t -10 -r 14 -f -O 0.05 -I 0.05
```

### Installation of AST-Monitor application
Since Raspberry Pi OS contains some technical limitations, AST-Monitor package cannot be installed directly using <i>pip</i> by executing the following command:
```sh
$ pip install ast-monitor
```

Instead of that, AST-Monitor has to be downloaded manually by cloning the GitHub repository:
```sh
$ cd /home/pi/
$ git clone https://github.com/firefly-cpp/AST-Monitor.git
```

By using packet managers apt and apt-get, you have to download PyQt5 distribution and additional packages for Raspberry Pi OS:
```sh
$ sudo apt-get install python3-pyqt5
$ sudo apt install python3-pyqt5.qtsvg
$ sudo apt-get install libatlas-base-dev
```

Furthermore, you have to download additional packages using pip:
```sh
$ pip install geopy
$ pip install --no-dependencies pyqt-feedback-flow
$ pip install sport-activities-features
$ pip install -U numpy
$ pip install pyusb
$ pip install adafruit-circuitpython-gps
```

OBSOLETE: [openant](https://github.com/Tigge/openant) package has to be downloaded and installed manually using these commands:
```sh
$ git clone https://github.com/Tigge/openant
$ cd ./openant/
$ sudo python setup.py install
```

### Automatic launch of AST-Monitor on start-up
In order to enable automatic launch of AST-Monitor application on start-up, the following line has to be appended to <i>/etc/xdg/lxsession/LXDE-pi/autostart</i>:
```
@python /home/pi/AST-Monitor/examples/run_example.py
```

### Automatic launch of scripts for reading GPS and heart rate data
To automatically launch the scripts that read and parse GPS and heart rate data, the following snippet has to be added to <i>/etc/profile</i>:
```sh
cd /home/pi/AST-Monitor/examples
nohup python /home/pi/AST-Monitor/examples/read_hr_data.py &
nohup python /home/pi/AST-Monitor/examples/read_gps_data.py &
```

Since by default, serial port 0 is disabled, you have to enable it by removing the line <i>console=serial0,115200</i> in <i>/boot/cmdline.txt</i>
