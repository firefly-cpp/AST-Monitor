import time
# it should work on arm architectures only
try:
    import board
except BaseException:
    pass

import busio
import serial
import adafruit_gps


class GpsSensor():
    """
    Class for working with GPS sensor.

    Args:
        gps_path: path to file for storing gps data
    """

    def __init__(self, gps_path="sensor_data/gps.txt"):
        """
        Initialisation method for GpsSensor class.

        Args:
            gps_path: path to file for storing gps data
        """
        self.gps_path = gps_path

    def write_gps_data_to_file(self, longitude, latitude, altitude):
        """
        Method for writing gps data to text file
        """

        output = str(longitude) + ";" + str(latitude) + ";" + str(altitude)
        with open(self.gps_path, 'a') as f:
            f.write(output + "\n")

    def get_gps_data(self):
        """
        Method for listening the channel for obtaining GPS data from sensor.

        Note: Example is based on source code from
        https://github.com/adafruit/Adafruit_CircuitPython_GPS
        """

        RX = board.RX
        TX = board.TX

        uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

        gps = adafruit_gps.GPS(uart, debug=False)

        gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

        gps.send_command(b'PMTK220,1000')

        last_print = time.monotonic()

        while True:

            gps.update()

            current = time.monotonic()
            if current - last_print >= 1.0:
                last_print = current
                if not gps.has_fix:
                    print('Waiting for fix...')
                    continue

                LATITUDE = gps.latitude
                LONGITUDE = gps.longitude
                ALTITUDE = gps.altitude_m

                if (LATITUDE is not None) and (
                        LONGITUDE is not None) and (ALTITUDE is not None):
                    self.write_gps_data_to_file(LONGITUDE, LATITUDE, ALTITUDE)
