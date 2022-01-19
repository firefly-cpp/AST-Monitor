from ant.easy.node import Node
from ant.easy.channel import Channel
from ant.base.message import Message

import logging
import struct
import threading
import sys
import os


class HrSensor():
    """
    Class for working with HR sensor.

    Args:
        hr_path: path to file for storing hr data
    """

    def __init__(self, hr_path="sensor_data/hr.txt"):
        """
        Initialisation method for HrSensor class.

        Args:
            hr_path: path to file for storing hr data
        """
        self.hr_path = hr_path

    def write_hr_data_to_file(self, hr):
        """
        Method for writing hr data to text file
        """
        with open(self.hr_path, 'a') as f:
            f.write(hr + "\n")

    def on_data(self, data):
        heartrate = data[7]
        print(heartrate)
        self.write_hr_data_to_file(str(heartrate))

    def get_hr_data(self):
        """
        Method for listening the channel for obtaining hr data from sensor.

        Note: Example is based on source code from
        https://github.com/Tigge/openant/blob/master/examples/heart_rate_monitor.py
        """

        NETWORK_KEY = [0xB9, 0xA5, 0x21, 0xFB, 0xBD, 0x72, 0xC3, 0x45]

        node = Node()
        node.set_network_key(0x00, NETWORK_KEY)

        channel = node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)

        channel.on_broadcast_data = self.on_data
        channel.on_burst_data = self.on_data

        channel.set_period(8070)
        channel.set_search_timeout(12)
        channel.set_rf_freq(57)
        channel.set_id(0, 120, 0)

        try:
            channel.open()
            node.start()
        finally:
            node.stop()
