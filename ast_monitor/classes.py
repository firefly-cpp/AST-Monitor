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
        total duration (float):
            the total duration in seconds
    """
    def __init__(
        self,
        average_heart_rate: float,
        total_duration: float
    ) -> None:
        """
        Initialization method for Interval class.\n
        Args:
            average_heart_rate (float):
                an average heart rate during an interval
            total duration (float):
                the total duration in seconds
        """
        self.average_heart_rate = average_heart_rate
        self.total_duration = total_duration

    def render(self, index: int) -> None:
        """
        Rendering an interval.
        """
        self.lbl_index = QLabel(str(index))
        self.lbl_index.setFont(QFont('Bahnschrift Semilight', 20))

        self.lbl_average_heart_rate = QLabel(
            str(self.average_heart_rate) + ' bpm'
        )
        self.lbl_average_heart_rate.setFont(QFont('Bahnschrift Semilight', 20))

        self.lbl_total_duration = QLabel(str(self.total_duration) + ' s')
        self.lbl_total_duration.setFont(QFont('Bahnschrift Semilight', 20))

        self.lyt_interval = QHBoxLayout()
        self.lyt_interval.addWidget(self.lbl_index)
        self.lyt_interval.addWidget(self.lbl_average_heart_rate)
        self.lyt_interval.addWidget(self.lbl_total_duration)

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
        lbl_index.setFont(QFont('Bahnschrift Semibold', 16))
        lbl_average_heart_rate = QLabel('Avg. heart rate')
        lbl_average_heart_rate.setFont(QFont('Bahnschrift Semibold', 16))
        lbl_duration = QLabel('Duration')
        lbl_duration.setFont(QFont('Bahnschrift Semibold', 16))
        lyt_title = QHBoxLayout()
        lyt_title.addWidget(lbl_index)
        lyt_title.addWidget(lbl_average_heart_rate)
        lyt_title.addWidget(lbl_duration)
        lyt_training_intervals.addLayout(lyt_title)

        index = 1
        for interval in intervals:
            i = Interval(
                interval['average_heart_rate'][0]['average_hr'],
                interval['total_duration'][0]['duration']
            )
            i.render(index)
            lyt_training_intervals.addLayout(i.lyt_interval)
            index += 1

        return lyt_training_intervals
