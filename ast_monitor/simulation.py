import sys
import time
import random
from tcxreader.tcxreader import TCXReader, TCXTrackPoint, TCXExercise


class Simulation():
    r"""Implementation of methods for simulating heart rate and gps data.

    Date:
        2021

    License:
        MIT
    """

    def __init__(self, hr_path="sensor_data/hr.txt",
                 gps_path="sensor_data/gps.txt"):
        self.hr_path = hr_path
        self.gps_path = gps_path

    def write_hr_to_file(self, hr):
        r"""Write hr simulation data to the text file."""
        with open(self.hr_path, 'a') as f:
            f.write(str(hr) + "\n")
            print("HR: " + str(hr))

    def write_gps_to_file(self, lon, lat, alt):
        r"""Write gps simulation data to the text file."""
        with open(self.gps_path, 'a') as f:
            f.write(str(lon) + ";" + lat + ";" + str(alt) + ";" + "\n")
            print("Lon: " + str(lon) + " Lat: " + str(lat))

    def simulate_hr(self):
        r"""Randomly generate heart rate between 150 and 160 beats per minute"""
        while True:
            time.sleep(1)
            new_rand = random.randint(150, 160)
            self.write_hr_to_file(new_rand)

    def simulate_gps(self):
        tcx_reader = TCXReader()
        file_location = 'dev/15.tcx'
        """
            TCX file test2.tcx was taken from the following dataset:
            S. Rauter, I. Jr. Fister, I. Fister. A collection of sport activity files
            for data analysis and data mining.
            Technical report 0201, University of Ljubljana and University of Maribor, 2015.
        """
        data: TCXExercise = tcx_reader.read(file_location)

        lon = []
        lat = []

        for i in range(len(data.trackpoints)):
            lat.append(str(data.trackpoints[i].latitude))
            lon.append(str(data.trackpoints[i].longitude))

        indexed = 0
        while True:
            time.sleep(5)
            self.write_gps_to_file(
                lon[indexed],
                lat[indexed],
                random.randint(
                    1,
                    3))
            indexed = indexed + 1
