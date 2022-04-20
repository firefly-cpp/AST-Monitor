# AST-Monitor --- A wearable Raspberry Pi computer for cyclists

---

[![PyPI Version](https://img.shields.io/pypi/v/ast-monitor.svg)](https://pypi.python.org/pypi/ast-monitor)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ast-monitor.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ast-monitor.svg)
[![Downloads](https://pepy.tech/badge/ast-monitor)](https://pepy.tech/project/ast-monitor)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/ast-monitor.svg)](https://github.com/firefly-cpp/AST-Monitor/blob/master/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/ast-monitor.svg)
![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/ast-monitor.svg)

[![DOI](https://img.shields.io/badge/DOI-10.1109/ISCMI53840.2021.9654817-blue)](https://doi.org/10.1109/ISCMI53840.2021.9654817)
[![Fedora package](https://img.shields.io/fedora/v/python3-ast-monitor?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-ast-monitor)

This repository is devoted to the AST-monitor, i.e., a low-cost and efficient embedded device for monitoring the realization of sports training sessions that are dedicated to monitoring cycling training sessions.
AST-Monitor is a part of the Artificial Sport Trainer (AST) system. The first bits of AST-monitor were presented in the following [paper](https://arxiv.org/abs/2109.13334).

## Outline of this repository

This repository presents basic code regarded to GUI. It was ported from the initial prototype to poetry.

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


A Serial Peripheral Interface (SPI) protocol was dedicated to communication between the Raspberry Pi and the GPS peripheral. A specialized USB ANT+ stick was used to capture the HR signal. The screen display was connected using a modified (physically shortened) HDMI cable, while the touch feedback was implemented using physical wires. The computer was powered during the testing phase using the Trust's (5 VDC) power bank. The AST-Monitor prototype is still a little bulky, but a more discrete solution is being searched for, including the sweat drainer of the AST.

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
| tcxreader       | ^0.3.8     | All      |
| sport-activities-features       | ^0.2.9     | All      |

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

## Deployment

Our project was deployed on a Raspberry Pi device using Raspbian OS.

### Run AST-Monitor on startup

Add the following lines in /etc/profile which ensures to run scripts on startup:

```sh
sudo python3 /home/user/run_example.py
sudo nohup python3 /home/user/read_hr_data.py  &
sudo nohup python3 /home/user/read_gps_data.py  &
```
## Examples

### Basic run

```python
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from ast_monitor.model import AST
import sys

# provide data locations

hr_data = "sensor_data/hr.txt"
gps_data = "sensor_data/gps.txt"


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data)

    window.show()
    sys.exit(app.exec_())
```


## License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

## Reference

Fister Jr, I., Fister, I., Iglesias, A., Galvez, A., Deb, S., & Fister, D. (2021). On deploying the Artificial Sport Trainer into practice. arXiv preprint [arXiv:2109.13334](https://arxiv.org/abs/2109.13334).
