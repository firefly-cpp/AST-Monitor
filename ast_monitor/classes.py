class SensorData():
    def __init__(self, hr, lon, lat, alt, curr_time) -> None:
        self.hr = hr
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.curr_time = curr_time


class Interval():
    def __init__(self, avhr, td) -> None:
        self.avhr = avhr
        self.td = td
