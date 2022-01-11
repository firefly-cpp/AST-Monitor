import time
try:
    import board
except:
    pass

import busio
import adafruit_gps

class GpsSensor():
    def __init__(self, gps_path = "sensor_data/gps.txt"):
        self.gps_path = gps_path

    def write_gps_data_to_file(longitude, latitude, altitude):
        zapis = str(longitude) + ";" + str(latitude) + ";" + str(altitude)
        with open(self.gps_path,'a') as f:
            f.write(zapis+"\n")

    # based on the example from https://github.com/adafruit/Adafruit_CircuitPython_GPS
    def get_gps_data(self):
        RX = board.RX
        TX = board.TX

        uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

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
                print('=' * 40)  # Print a separator line.
                print('Latitude: {0:.6f} degrees'.format(gps.latitude))
                print('Longitude: {0:.6f} degrees'.format(gps.longitude))

                LATITUDE = gps.latitude
                LONGITUDE = gps.longitude
                ALTITUDE = gps.altitude_m

                if (LATITUDE != None) and (LONGITUDE != None) and (ALTITUDE != None):
                    self.write_gps_data_to_file(LONGITUDE, LATITUDE, ALTITUDE)
