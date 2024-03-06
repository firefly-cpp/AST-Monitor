AST-Monitor documentation!
========================================

.. automodule:: ast_monitor

AST-Monitor is a wearable Raspberry Pi computer for cyclists.

* **Free software:** MIT license
* **Github repository:** https://github.com/firefly-cpp/AST-Monitor
* **Python versions:** 3.6.x, 3.7.x, 3.8.x, 3.9.x, 3.10.x, 3.11.x, 3.12.x

Short description
-----------------

Welcome to AST-Monitor: Revolutionizing Sport Training Sessions! 🏋️‍♂️

This repository aims to introduce a low-cost, and efficient embedded device that can transform the way you monitor cycling training sessions. Allow us to present AST-Monitor.

To begin, we invite you to explore the paper that introduces the capabilities of AST-Monitor. Dive into the future of artificial sports trainers by reading this `paper <https://arxiv.org/abs/2109.13334>`_. 📄💡

Graphical User Interface of the application
-------------------------------------------

Basic data: Power at Your Fingertips 💪
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://user-images.githubusercontent.com/73126820/179205064-160bdd44-fd67-4d8d-85dd-badea999885c.png

The initial page of the AST-Monitor application presents essential parameters, providing real-time insights into an athlete's performance. Gain access to information such as the athlete's current speed and heart rate. After a training session, you'll also receive a comprehensive overview, including total distance covered, session duration, and total ascent conquered. 📱🚴‍♂️

Interactive map: Embark on a Visual Journey 🗺️🚀
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://github.com/alenrajsp/AST-Monitor/blob/main/.github/img/route3.png?raw=true

As you navigate uncharted territories, this map reveals your precise location in real-time. And allows you to track your progress on the route in real time. 🌍🚴‍♂️🗺️

Interval training data: Unleash Your Inner Athlete 🏃‍♀️💪
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://user-images.githubusercontent.com/73126820/179205160-edce581c-1ea8-4287-a795-7d05fb7c8ddc.png

Discover the duration of each phase, track your current heart rate, and marvel at the average heart rate achieved. But that's not all—brace yourself for the Digital Twin proposed heart rate and witness the thrilling difference between your current heart rate and the proposed target. Prepare to dominate your workouts with the AST-Monitor! 🏋️‍♀️

Interval training plan: Unleash the Potential 💯📝💥
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://user-images.githubusercontent.com/73126820/189926103-e0895132-9bbc-41bf-8868-51e3e6c23f8a.png

Load up and embark on thrilling interval trainings that await you in the ``AST-Monitor/development/trainings`` folder. These trainings, meticulously crafted in the domain-specific language `AST-TDL <https://github.com/firefly-cpp/ast-tdl>`_, are designed to take you to the next level. Once successfully loaded, witness the training plan come to life before your eyes. 🚀📋💥

Hardware outline: Where Innovation Meets Performance ⚙️🔩💡
-----------------------------------------------------------

Prepare to be dazzled by the complete hardware setup featured in AST-Monitor.

.. image:: https://raw.githubusercontent.com/firefly-cpp/AST-Monitor/main/.github/img/complete_small.JPG

Let's take a closer look at the components:


- **A platform with fixing straps** that securely attach to your bicycle, ensuring a seamless training experience. 🚲🔒
- **The powerful Raspberry Pi 4 Model B micro-controller**, powered by the dynamic Raspbian OS. 💻
- **A five-inch LCD touch screen display**, allowing the interaction with AST-Monitor during the training. ✨🖥️
- **Equipped with a USB ANT+ stick**, AST-Monitor captures the heartbeat of your training, providing crucial data for your journey to greatness. 📡
- **Adafruit's Ultimate GPS HAT module** joins the lineup, empowering you with location information and paving the way for GPS integration (coming soon!). 🌐🛰️

But that's not all:

A Serial Peripheral Interface (SPI) protocol ensures seamless communication between the Raspberry Pi and the GPS peripheral, guaranteeing accurate and timely data. The screen display, connected using a physically shortened HDMI cable, ensures a sleek and compact design that doesn't compromise performance.

During the testing phase, the AST-Monitor prototype was powered by Trust's 5 VDC power bank, providing unparalleled endurance. While the current prototype may be a bit bulky, rest assured, our team is hard at work, exploring sleeker and more discreet solutions. 💪💦

For those who crave a glimpse inside AST-Monitor:

.. image:: https://user-images.githubusercontent.com/73126820/189920171-ac946a93-ad78-4e4b-bf09-5de5bf69bef9.png

Welcome to the next stage of sports training. Welcome to AST-Monitor—your ultimate companion on the road to victory! 🌟🏆🚀

Documentation
-------------

The main documentation is organized into a couple of sections:

* :ref:`user-docs`
* :ref:`dev-docs`
* :ref:`about-docs`

.. _user-docs:

.. toctree::
   :maxdepth: 3
   :caption: User Documentation

   getting_started

.. _dev-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   installation
   testing
   documentation
   api/index

.. _about-docs:

.. toctree::
   :maxdepth: 3
   :caption: About

   contributing
   code_of_conduct
