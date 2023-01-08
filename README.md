# AST-Monitor --- A wearable Raspberry Pi computer for cyclists
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![PyPI Version](https://img.shields.io/pypi/v/ast-monitor.svg)](https://pypi.python.org/pypi/ast-monitor)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ast-monitor.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ast-monitor.svg)
[![Downloads](https://pepy.tech/badge/ast-monitor)](https://pepy.tech/project/ast-monitor)
![GitHub repo size](https://img.shields.io/github/repo-size/firefly-cpp/ast-monitor?style=flat-square)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/ast-monitor.svg)](https://github.com/firefly-cpp/AST-Monitor/blob/master/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/ast-monitor.svg)
![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/ast-monitor.svg)

[![DOI](https://img.shields.io/badge/DOI-10.1109/ISCMI53840.2021.9654817-blue)](https://doi.org/10.1109/ISCMI53840.2021.9654817)
[![DOI](https://img.shields.io/badge/DOI-10.3390/app122412741-blue)](https://doi.org/10.3390/app122412741)
[![Fedora package](https://img.shields.io/fedora/v/python3-ast-monitor?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-ast-monitor)
[![AUR package](https://img.shields.io/aur/version/python-ast-monitor?color=blue&label=Arch%20Linux&logo=arch-linux)](https://aur.archlinux.org/packages/python-ast-monitor)

## Short description
This repository is devoted to AST-Monitor, i.e., a low-cost and efficient embedded device for monitoring the realization of sport training sessions that are dedicated to monitoring cycling training sessions.
AST-Monitor is a part of the Artificial Sport Trainer (AST) system. The first bits of AST-Monitor were presented in the following [paper](https://arxiv.org/abs/2109.13334).


## Graphical User Interface of the application
### Basic data
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205064-160bdd44-fd67-4d8d-85dd-badea999885c.png" alt="AST-GUI">
</p>
The initial page of the application depicts basic parameters of an athlete's activity: current speed and current heart rate. If a training session is conducted, total distance, total time of the session and total ascent are displayed as well.

---
### Interactive map
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205118-19cbb6e2-f410-4371-a762-c4c77344ab24.png" alt="AST-Map">
</p>
The second page of the application is devoted to an interactive map, which depicts athlete's current position.

Note: the position is currently hardcoded and does not respond according to GPS data.

---
### Interval training data
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205160-edce581c-1ea8-4287-a795-7d05fb7c8ddc.png" alt="AST-Intervals">
</p>
The third page of the application depicts interval training data. During an interval training, total duration of the current phase is displayed along with current heart rate, average heart rate, Digital Twin proposed heart rate and the difference between the current and the proposed heart rate.

---
### Interval training plan
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/189926103-e0895132-9bbc-41bf-8868-51e3e6c23f8a.png" alt="AST-Trainings">
</p>
The fourth and final page of the application is intended for loading and starting interval trainings located in the folder "AST-Monitor/development/trainings". In order to be parsed correctly, trainings must be written in domain-specific language <a href="https://github.com/firefly-cpp/ast-tdl">AST-TDL</a> and converted to JavaScript Object Notation (JSON). After successful loading of an interval training, the training plan is displayed on this page.


## Hardware outline
The complete hardware part is shown in the figure from which it can be seen that the AST-computer is split into the following pieces:

* a platform with fixing straps that attach to a bicycle,
* the Raspberry Pi 4 Model B micro-controller with Raspbian OS installed,
* a five-inch LCD touch screen display,
* a USB ANT+ stick,
* Adafruit's Ultimate GPS HAT module.

<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/firefly-cpp/AST-Monitor/main/.github/img/complete_small.JPG" alt="AST-Monitor">
</p>

A Serial Peripheral Interface (SPI) protocol was dedicated to communication between the Raspberry Pi and the GPS peripheral. A specialized USB ANT+ stick was used to capture the HR signal. The screen display was connected using a modified (physically shortened) HDMI cable, while the touch feedback was implemented using physical wires. The computer was powered during the testing phase using the Trust's (5 VDC) power bank. The AST-Monitor prototype is still a little bulky, but a more discrete solution is being searched for, including the sweat drainer of the AST. Internal components of AST-Monitor are depicted in the following scheme.

<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/189920171-ac946a93-ad78-4e4b-bf09-5de5bf69bef9.png" alt="AST-Monitor">
</p>

## Software outline
### Dependencies
List of dependencies:

| Package      | Version    | Platform |
| ------------ |:----------:|:--------:|
| PyQt5        | ^5.15.6    | All      |
| matplotlib   | ^3.5.1     | All      |
| geopy        | ^2.2.0     | All      |
| openant        | v0.4     | All      |
| pyqt-feedback-flow       | ^0.1.0     | All      |
| tcxreader       | ^0.4.1     | All      |
| sport-activities-features       | ^0.3.6     | All      |

Note: openant package should be installed manually. Please follow the [official instructions](https://github.com/Tigge/openant). If you use Fedora OS, you can install openant package using the dnf package manager:

```sh
$ dnf install python-openant
```

Additional note: adafruit-circuitpython-gps package must be installed in order to work with the GPS sensor:

```sh
$ pip install adafruit-circuitpython-gps
```

## Installation
Install AST-Monitor with pip:

```sh
$ pip install ast-monitor
```
In case you want to install directly from the source code, use:

```sh
$ git clone https://github.com/firefly-cpp/AST-Monitor.git
$ cd AST-Monitor
$ poetry build
$ python setup.py install
```

To install AST-Monitor on Fedora Linux, please use:

```sh
$ dnf install python3-ast-monitor
```

To install AST-Monitor on Alpine Linux, please use:

```sh
$ apk add py3-ast-monitor
```

To install AST-Monitor on Arch Linux, please use an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):

```sh
$ yay -Syyu python-ast-monitor
```

## Deployment
Our project was deployed on a Raspberry Pi device using Raspberry Pi OS.

The hardware configuration of AST-Monitor using Raspberry Pi OS is described in <a href="https://github.com/firefly-cpp/AST-Monitor/blob/main/HARDWARE_CONFIGURATION.md">HARDWARE_CONFIGURATION.md</a>.

## Examples

### Basic run
```python
from PyQt5 import QtWidgets
import sys

try:
    from ast_monitor.model import AST
except ModuleNotFoundError:
    sys.path.append('../')
    from ast_monitor.model import AST


# Paths to the files with heart rates and GPS data.
hr_data = '../sensor_data/hr.txt'
gps_data = '../sensor_data/gps.txt'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data)
    window.show()
    sys.exit(app.exec_())
```

## License
This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer
This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

## Cite us
Lukač, L., Fister Jr., I., Fister, I. "[Digital Twin in Sport: From an Idea to Realization](https://www.mdpi.com/2076-3417/12/24/12741)." Applied Sciences 12.24 (2022): 12741.

## References
Fister Jr, I., Fister, I., Iglesias, A., Galvez, A., Deb, S., & Fister, D. (2021). On deploying the Artificial Sport Trainer into practice. arXiv preprint [arXiv:2109.13334](https://arxiv.org/abs/2109.13334).

Fister Jr, I., Salcedo-Sanz, S., Iglesias, A., Fister, D., Gálvez, A., & Fister, I. (2021). New Perspectives in the Development of the Artificial Sport Trainer. Applied Sciences, 11(23), 11452. DOI: [10.3390/app112311452](https://doi.org/10.3390/app112311452)

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="http://www.iztok-jr-fister.eu/"><img src="https://avatars.githubusercontent.com/u/1633361?v=4?s=100" width="100px;" alt="Iztok Fister Jr."/><br /><sub><b>Iztok Fister Jr.</b></sub></a><br /><a href="https://github.com/firefly-cpp/AST-Monitor/issues?q=author%3Afirefly-cpp" title="Bug reports">🐛</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=firefly-cpp" title="Documentation">📖</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=firefly-cpp" title="Code">💻</a> <a href="#maintenance-firefly-cpp" title="Maintenance">🚧</a> <a href="#mentoring-firefly-cpp" title="Mentoring">🧑‍🏫</a> <a href="#platform-firefly-cpp" title="Packaging/porting to new platform">📦</a></td>
      <td align="center"><a href="https://github.com/luckyLukac"><img src="https://avatars.githubusercontent.com/u/73126820?v=4?s=100" width="100px;" alt="luckyLukac"/><br /><sub><b>luckyLukac</b></sub></a><br /><a href="https://github.com/firefly-cpp/AST-Monitor/issues?q=author%3AluckyLukac" title="Bug reports">🐛</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=luckyLukac" title="Documentation">📖</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=luckyLukac" title="Code">💻</a> <a href="#design-luckyLukac" title="Design">🎨</a></td>
      <td align="center"><a href="http://carlosal1015.github.io"><img src="https://avatars.githubusercontent.com/u/21283014?v=4?s=100" width="100px;" alt="Oromion"/><br /><sub><b>Oromion</b></sub></a><br /><a href="#platform-carlosal1015" title="Packaging/porting to new platform">📦</a></td>
      <td align="center"><a href="https://github.com/alenrajsp"><img src="https://avatars.githubusercontent.com/u/27721714?v=4?s=100" width="100px;" alt="alenrajsp"/><br /><sub><b>alenrajsp</b></sub></a><br /><a href="#content-alenrajsp" title="Content">🖋</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
