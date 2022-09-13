import time

# It should work on ARM architectures only.
try:
    import adafruit_gps
    import serial
except BaseException:
    pass


class GpsSensor:
    """
    Class for working with GPS sensor.\n
    Args:
        gps_path (str):
            path to file for storing GPS data
    """
    def __init__(self, gps_path: str = 'sensor_data/gps.txt') -> None:
        """
        Initialisation method for GpsSensor class.\n
        Args:
            gps_path (str):
                path to file for storing gps data
        """
        self.gps_path = gps_path

    def write_gps_data_to_file(
        self,
        longitude: float,
        latitude: float,
        altitude: float
    ) -> None:
        """
        Method for writing GPS data to text file.\n
        Args:
            longitude (float):
                longitude on Earth
            latitude (float):
                latitude on Earth
            altitude (float):
                current altitude
        """
        output = (
            str(longitude) + ';' + str(latitude) + ';' +
            str(altitude) + ';' + time.time()
        )
        with open(self.gps_path, 'a') as f:
            f.write(output + '\n')

    def get_gps_data(self) -> None:
        """
        Method for listening the channel for obtaining GPS data from sensor.\n
        Note: Example is based on source code from
              https://github.com/adafruit/Adafruit_CircuitPython_GPS
        """
        uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=10)
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

                if (
                    (LATITUDE is not None) and
                    (LONGITUDE is not None) and
                    (ALTITUDE is not None)
                ):
                    self.write_gps_data_to_file(LONGITUDE, LATITUDE, ALTITUDE)
