from tcxreader.tcxreader import TCXReader
import time


class Simulation():
    """
    Implementation of methods for simulating heart rate and GPS data.\n
    Args:
        hr_path (str):
            path to the file with heart rates
        gps_path (str):
            path to the file with GPS data
    Date:
        2021
    License:
        MIT
    """
    def __init__(
        self,
        hr_path='../sensor_data/hr.txt',
        gps_path='../sensor_data/gps.txt'
    ) -> None:
        """
        Initialisation method for Simulation class.\n
        Args:
            hr_path (str):
                path to the file with heart rates
            gps_path (str):
                path to the file with GPS data
        """
        self.hr_path = hr_path
        self.gps_path = gps_path

    def write_hr_to_file(self, hr: int) -> None:
        """
        Write HR simulation data to the text file.\n
        Args:
            hr (int):
                heart rate
        """
        with open(self.hr_path, 'a') as f:
            f.write(str(hr) + '\n')
            print('HR: ' + str(hr))

    def write_gps_to_file(self, lon: float, lat: float, alt: float) -> None:
        """
        Write GPS simulation data to the text file.\n
        Args:
            lon (float):
                longitude on Earth
            lat (float):
                latitude on Earth
            alt (float):
                current altitude
        """
        with open(self.gps_path, 'a') as f:
            f.write(
                str(lon) + ';' + lat + ';' + str(alt) + ';' +
                str(time.time()) + '\n'
            )
            print('Lon: ' + str(lon) + ' Lat: ' + str(lat))

    def simulate_hr(self) -> None:
        """
        Randomly generate heart rate between 150 and 160 beats per minute.
        """
        while True:
            for i in range(25):
                time.sleep(1)
                new_rand = int(float(150 + (i / 25) * 15))
                self.write_hr_to_file(new_rand)

            for i in range(25):
                time.sleep(1)
                new_rand = int(float(150 + ((25 - i) / 25) * 15))
                self.write_hr_to_file(new_rand)

            for i in range(25):
                time.sleep(1)
                new_rand = int(float(80 + ((25 - i) / 25) * 70))
                self.write_hr_to_file(new_rand)

            for i in range(25):
                time.sleep(1)
                new_rand = int(float(80 + (i / 25) * 20))
                self.write_hr_to_file(new_rand)

    def simulate_gps(self) -> None:
        """
        GPS simulation.
        """
        tcx_reader = TCXReader()
        file_location = '../development/datasets/15.tcx'
        """
            TCX file test2.tcx was taken from the following dataset:
            S. Rauter, I. Jr. Fister, I. Fister.

            A collection of sport activity files
            for data analysis and data mining.

            Technical report 0201, University of Ljubljana
            and University of Maribor, 2015.
        """
        data = tcx_reader.read(file_location)

        for i in range(len(data.trackpoints)):
            time.sleep(1)
            self.write_gps_to_file(
                str(data.trackpoints[i].longitude),
                str(data.trackpoints[i].latitude),
                str(data.trackpoints[i].elevation)
            )
