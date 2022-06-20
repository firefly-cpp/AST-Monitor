from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout


class SensorData:
    """
    Class for storing the captured sensor data.\n
    Args:
        heart_rate (int):
            the current heart rate in beats per minute
        longitude (float):
            the current longitude in degrees
        latitude (float):
            the current latitude in degrees
        time ():
            XXX
        distance (float):
            the current cummulative distance in meters
    """
    def __init__(
        self,
        heart_rate: int,
        longitude: float,
        latitude: float,
        altitude: float,
        time,
        distance: float
    ) -> None:
        """
        Initialization method for SensorData class.\n
        Args:
            heart_rate (int):
                the current heart rate in beats per minute
            longitude (float):
                the current longitude in degrees
            latitude (float):
                the current latitude in degrees
            time ():
                XXX
            distance (float):
                the current cummulative distance in meters
        """
        self.heart_rate = heart_rate
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.time = time
        self.distance = distance


class Interval:
    """
    Class for storing intervals.\n
    Args:
        average_heart_rate (float):
            an average heart rate during an interval
        total distance (float):
            the total distance in meters
    """
    def __init__(
        self,
        average_heart_rate: float,
        total_distance: float
    ) -> None:
        """
        Initialization method for Interval class.\n
        Args:
            average_heart_rate (float):
                an average heart rate during an interval
            total distance (float):
                the total distance in meters
        """
        self.average_heart_rate = average_heart_rate
        self.total_distance = total_distance

    def render(self, index: int) -> None:
        """
        Rendering an interval.
        """
        self.lbl_index = QLabel(str(index))
        self.lbl_index.setFont(QFont('Bahnschrift Semilight', 20))
        # self.lbl_index.setStyleSheet('border: 1px solid black')

        self.lbl_average_heart_rate = QLabel(str(self.average_heart_rate))
        self.lbl_average_heart_rate.setFont(QFont('Bahnschrift Semilight', 20))
        # self.lbl_average_heart_rate.setStyleSheet('border: 1px solid black')

        self.lyt_interval = QHBoxLayout()
        self.lyt_interval.addWidget(self.lbl_index)
        self.lyt_interval.addWidget(self.lbl_average_heart_rate)

    @staticmethod
    def render_intervals(intervals: list) -> QVBoxLayout:
        """
        Rendering all intervals from the list.\n
        Args:
            intervals (list):
                list of intervals to be rendered
        Returns:
            QVBoxLayout: layout with intervals
        """
        lyt_training_intervals = QVBoxLayout()
        lyt_training_intervals.setContentsMargins(40, 0, 40, 0)

        # Adding title.
        lbl_index = QLabel('Index')
        lbl_index.setFont(QFont('Bahnschrift Semibold', 20))
        # lbl_index.setStyleSheet('border: 1px solid black')
        lbl_average_heart_rate = QLabel('Average heart rate')
        lbl_average_heart_rate.setFont(QFont('Bahnschrift Semibold', 20))
        # lbl_average_heart_rate.setStyleSheet('border: 1px solid black')
        lyt_title = QHBoxLayout()
        lyt_title.addWidget(lbl_index)
        lyt_title.addWidget(lbl_average_heart_rate)
        lyt_training_intervals.addLayout(lyt_title)

        index = 1
        for interval in intervals:
            i = Interval(interval['average_heart_rate'][0]['average_hr'], 0.0)
            i.render(index)
            lyt_training_intervals.addLayout(i.lyt_interval)
            index += 1

        return lyt_training_intervals
