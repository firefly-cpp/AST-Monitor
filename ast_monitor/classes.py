class SensorData():
    def __init__(self, hr, lon, lat, alt, curr_time, dist) -> None:
        self.hr = hr
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.curr_time = curr_time
        self.dist = dist


class Interval():
    def __init__(self, avhr, td) -> None:
        self.avhr = avhr
        self.td = td
