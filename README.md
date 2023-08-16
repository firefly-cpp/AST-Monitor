<p align="center">
  <img width="300" src=".github/img/logo.png" alt="logo.png">
</p>

# AST-Monitor --- A wearable Raspberry Pi computer for cyclists
[![PyPI Version](https://img.shields.io/pypi/v/ast-monitor.svg)](https://pypi.python.org/pypi/ast-monitor)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ast-monitor.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ast-monitor.svg)
[![Downloads](https://pepy.tech/badge/ast-monitor)](https://pepy.tech/project/ast-monitor)
![GitHub repo size](https://img.shields.io/github/repo-size/firefly-cpp/ast-monitor?style=flat-square)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/ast-monitor.svg)](https://github.com/firefly-cpp/AST-Monitor/blob/master/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/ast-monitor.svg)
![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/ast-monitor.svg)
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)

[![DOI](https://img.shields.io/badge/DOI-10.1109/ISCMI53840.2021.9654817-blue)](https://doi.org/10.1109/ISCMI53840.2021.9654817)
[![DOI](https://img.shields.io/badge/DOI-10.3390/app122412741-blue)](https://doi.org/10.3390/app122412741)
[![Fedora package](https://img.shields.io/fedora/v/python3-ast-monitor?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-ast-monitor)
[![AUR package](https://img.shields.io/aur/version/python-ast-monitor?color=blue&label=Arch%20Linux&logo=arch-linux)](https://aur.archlinux.org/packages/python-ast-monitor)

* **Documentation:** [https://ast-monitor.readthedocs.io/en/latest](https://ast-monitor.readthedocs.io/en/latest)
* **Tested OS:** Windows, Ubuntu, Fedora, Alpine, Arch, macOS. **However, that does not mean it does not work on others**

## Short description
Welcome to AST-Monitor: Revolutionizing Sport Training Sessions! 🏋️‍♂️

This repository is not an ordinary tech project—it aims to introduce a cutting-edge, low-cost, and highly efficient embedded device that can transform the way you monitor cycling training sessions. Allow us to present AST-Monitor, a significant achievement within the Artificial Sport Trainer (AST) system. :gem:🔥

To begin, we invite you to explore the paper that introduces the remarkable capabilities of AST-Monitor. Delve into the future of sports training by reading this captivating [paper](https://arxiv.org/abs/2109.13334). 📄💡

## Graphical User Interface of the application
### Basic data: Power at Your Fingertips 💪
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205064-160bdd44-fd67-4d8d-85dd-badea999885c.png" alt="AST-GUI">
</p>
The initial page of the AST-Monitor application presents essential parameters, providing real-time insights into an athlete's performance. Gain access to information such as the athlete's current speed and heart rate. But that's not all! After a training session, you'll also receive a comprehensive overview, including total distance covered, session duration, and total ascent conquered. It's like having a personal trainer right in your pocket! 📱🚴‍♂️

---

### Interactive map: Embark on a Visual Journey 🗺️🚀
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205118-19cbb6e2-f410-4371-a762-c4c77344ab24.png" alt="AST-Map">
</p>
Ready for an adventure? Brace yourself for the second page of the AST-Monitor application—a mesmerizing interactive map. As you navigate uncharted territories, this map reveals your precise location in real-time. Experience the thrill as you watch your avatar progress along the route.  🌍🚴‍♂️🗺️

Note: The position is currently hardcoded and does not respond according to GPS data.

---

### Interval training data: Unleash Your Inner Athlete 🏃‍♀️💪
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/179205160-edce581c-1ea8-4287-a795-7d05fb7c8ddc.png" alt="AST-Intervals">
</p>
The third page of the AST-Monitor application caters to interval training enthusiasts. With interval training data at your fingertips, you'll stay at the top of your game like never before. Discover the duration of each phase, track your current heart rate, and marvel at the average heart rate achieved. But that's not all—brace yourself for the Digital Twin proposed heart rate and witness the thrilling difference between your current heart rate and the proposed target. Prepare to dominate your workouts with the AST-Monitor! 🏋️‍♀️

---

### Interval training plan: Unleash the Potential 💯📝💥
<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/189926103-e0895132-9bbc-41bf-8868-51e3e6c23f8a.png" alt="AST-Trainings">
</p>
Ladies and gentlemen, we present to you the fourth and final page of the AST-Monitor application—a gateway to unparalleled training excellence. Load up and embark on thrilling interval trainings that await you in the "AST-Monitor/development/trainings" folder. These trainings, meticulously crafted in the domain-specific language <a href="https://github.com/firefly-cpp/ast-tdl">AST-TDL</a>, are designed to take you to the next level. Once successfully loaded, witness the training plan come to life before your eyes. Get ready to elevate your performance with the AST-Monitor! 🚀📋💥

## Hardware outline: Where Innovation Meets Performance ⚙️🔩💡
Prepare to be dazzled by the complete hardware setup featured in AST-Monitor.

<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/firefly-cpp/AST-Monitor/main/.github/img/complete_small.JPG" alt="AST-Monitor">
</p>

Let's take a closer look at the impressive components that make up this technological marvel:

* **A platform with fixing straps** that securely attach to your bicycle, ensuring a seamless training experience. 🚲🔒
* **The powerful Raspberry Pi 4 Model B micro-controller**, powered by the dynamic Raspbian OS. 💻
* **A five-inch LCD touch screen display**, where the magic happens and wonders unfold. ✨🖥️
* **Equipped with a USB ANT+ stick**, AST-Monitor captures the heartbeat of your training, providing crucial data for your journey to greatness. 📡
* **Adafruit's Ultimate GPS HAT module** joins the lineup, empowering you with location information and paving the way for GPS integration (coming soon!). 🌐🛰️

But that's not all—AST-Monitor's engineering prowess shines through in every detail:

A Serial Peripheral Interface (SPI) protocol ensures seamless communication between the Raspberry Pi and the GPS peripheral, guaranteeing accurate and timely data. The screen display, connected using a physically shortened HDMI cable, ensures a sleek and compact design that doesn't compromise performance. Oh, and did we mention the touch feedback? The seamless touch experience is brought to life through intricate physical wiring.

During the testing phase, the AST-Monitor prototype was powered by Trust's 5 VDC power bank, providing unparalleled endurance. While the current prototype may be a bit bulky, rest assured, our team is hard at work, exploring sleeker and more discreet solutions, including the sweat drainer of the AST. 💪💦

For those who crave a glimpse inside this technological marvel, behold the intricate internal components of AST-Monitor:

<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/73126820/189920171-ac946a93-ad78-4e4b-bf09-5de5bf69bef9.png" alt="AST-Monitor">
</p>

Welcome to the future of sports training. Welcome to AST-Monitor—your ultimate companion on the road to victory! 🌟🏆🚀

## Software outline
### Dependencies
List of dependencies:

| Package      | Version    | Platform |
| ------------ |:----------:|:--------:|
| PyQt5        | ^5.15.6    | All      |
| matplotlib   | ^3.5.1     | All      |
| geopy        | ^2.2.0     | All      |
| openant      | ^1.2.0     | All      |
| pyqt-feedback-flow       | ^0.1.0     | All      |
| tcxreader       | ^0.4.1     | All      |
| sport-activities-features       | ^0.3.6     | All      |

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
      <td align="center" valign="top" width="14.28%"><a href="http://www.iztok-jr-fister.eu/"><img src="https://avatars.githubusercontent.com/u/1633361?v=4?s=100" width="100px;" alt="Iztok Fister Jr."/><br /><sub><b>Iztok Fister Jr.</b></sub></a><br /><a href="https://github.com/firefly-cpp/AST-Monitor/issues?q=author%3Afirefly-cpp" title="Bug reports">🐛</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=firefly-cpp" title="Documentation">📖</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=firefly-cpp" title="Code">💻</a> <a href="#maintenance-firefly-cpp" title="Maintenance">🚧</a> <a href="#mentoring-firefly-cpp" title="Mentoring">🧑‍🏫</a> <a href="#platform-firefly-cpp" title="Packaging/porting to new platform">📦</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luckyLukac"><img src="https://avatars.githubusercontent.com/u/73126820?v=4?s=100" width="100px;" alt="luckyLukac"/><br /><sub><b>luckyLukac</b></sub></a><br /><a href="https://github.com/firefly-cpp/AST-Monitor/issues?q=author%3AluckyLukac" title="Bug reports">🐛</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=luckyLukac" title="Documentation">📖</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=luckyLukac" title="Code">💻</a> <a href="#design-luckyLukac" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://carlosal1015.github.io"><img src="https://avatars.githubusercontent.com/u/21283014?v=4?s=100" width="100px;" alt="Oromion"/><br /><sub><b>Oromion</b></sub></a><br /><a href="#platform-carlosal1015" title="Packaging/porting to new platform">📦</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alenrajsp"><img src="https://avatars.githubusercontent.com/u/27721714?v=4?s=100" width="100px;" alt="alenrajsp"/><br /><sub><b>alenrajsp</b></sub></a><br /><a href="#content-alenrajsp" title="Content">🖋</a> <a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=alenrajsp" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/KukovecRok"><img src="https://avatars.githubusercontent.com/u/33880044?v=4?s=100" width="100px;" alt="Tatookie"/><br /><sub><b>Tatookie</b></sub></a><br /><a href="https://github.com/firefly-cpp/AST-Monitor/commits?author=KukovecRok" title="Documentation">📖</a> <a href="https://github.com/firefly-cpp/AST-Monitor/issues?q=author%3AKukovecRok" title="Bug reports">🐛</a></td>
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
