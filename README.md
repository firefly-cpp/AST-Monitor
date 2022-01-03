# AST-Monitor --- A wearable Raspberry Pi computer for cyclists

This repository is devoted to the AST-monitor, i.e. a low-cost and efficient embedded device for monitoring the realization of sport training sessions that is dedicated to monitor cycling training sessions.
AST-Monitor is a part of Artificial Sport Trainer (AST) system. First bits of AST-monitor were presented in the following [paper](https://arxiv.org/abs/2109.13334). 

## Outline of this repository

This repository presents basic code regarded to GUI. It was ported from the initial prototype to poetry.

## Hardware outline 

The complete hardware part is shown in Fig from which it can be seen that the AST-computer is split into the following pieces: 

* a platform with fixing straps that attach to a bicycle,
* the Raspberry Pi 4 Model B micro-controller with Raspbian OS installed,
* a five-inch LCD touch screen display,
* a USB ANT stick,
* Adafruit's Ultimate GPS HAT module.

<p align="center">
  <img width="200" src="img/complete_small.JPG">
</p>


A Serial Peripheral Interface (SPI) protocol was dedicated for communication between the Raspberry Pi and the GPS peripheral. A specialized USB ANT stick was used to capture the HR signal. The screen display was connected using a modified (physically shortened) HDMI cable, while the touch feedback was implemented using physical wires. The computer was powered during the testing phase using the Trust's (5 VDC) power-bank. The AST-Monitor prototype is still a little bulky, but a more discrete solution is being searched for, including the sweat drainer of the AST.

## Software outline

### Software libraries

Note: openant package should be installed manually. Please follow to the [official instructions](https://github.com/Tigge/openant).

## Deployment


## Licence

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

## Reference

Fister Jr, I., Fister, I., Iglesias, A., Galvez, A., Deb, S., & Fister, D. (2021). On deploying the Artificial Sport Trainer into practice. arXiv preprint [arXiv:2109.13334](https://arxiv.org/abs/2109.13334).
