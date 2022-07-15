from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from sport_activities_features.training_loads import BanisterTRIMP


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
        speed_duration (int):
            duration of a speed segment of the interval in minutes
        recovery_duration (int):
            duration of a recovery segment of the interval in minutes
        speed_heart_rate (int):
            planned average heart rate during
            a speed segment of the interval
        recovery_heart_rate (int):
            planned average heart rate during
            a recovery segment of the interval
    """
    def __init__(
        self,
        speed_duration: int,
        recovery_duration: int,
        speed_heart_rate: int,
        recovery_heart_rate: int
    ) -> None:
        """
        Initialization method for Interval class.\n
        Args:
            speed_duration (int):
                duration of a speed segment of the interval in minutes
            recovery_duration (int):
                duration of a recovery segment of the interval in minutes
            speed_heart_rate (int):
                planned average heart rate during
                a speed segment of the interval
            recovery_heart_rate (int):
                planned average heart rate during
                a recovery segment of the interval
        """
        self.speed_duration = speed_duration
        self.recovery_duration = recovery_duration
        self.speed_heart_rate = speed_heart_rate
        self.recovery_heart_rate = recovery_heart_rate
        banister = BanisterTRIMP(speed_duration, speed_heart_rate)
        self.planned_TRIMP = banister.calculate_TRIMP()

    def render(self, index: int) -> None:
        """
        Rendering an interval.
        """
        self.lbl_index = QLabel(str(index))
        self.lbl_index.setFont(QFont('Bahnschrift Semilight', 15))

        self.lbl_speed_heart_rate = QLabel(str(self.speed_heart_rate))
        self.lbl_speed_heart_rate.setFont(QFont('Bahnschrift Semilight', 15))
        self.lbl_speed_duration = QLabel(str(self.speed_duration) + ' min')
        self.lbl_speed_duration.setFont(QFont('Bahnschrift Semilight', 15))

        self.lbl_recovery_heart_rate = QLabel(str(self.recovery_heart_rate))
        self.lbl_recovery_heart_rate.setFont(
            QFont('Bahnschrift Semilight', 15)
        )
        self.lbl_recovery_duration = QLabel(
            str(self.recovery_duration) + ' min'
        )
        self.lbl_recovery_duration.setFont(QFont('Bahnschrift Semilight', 15))

        self.lyt_interval = QHBoxLayout()
        self.lyt_interval.addWidget(self.lbl_index)
        self.lyt_interval.addWidget(self.lbl_speed_heart_rate)
        self.lyt_interval.addWidget(self.lbl_speed_duration)
        self.lyt_interval.addWidget(self.lbl_recovery_heart_rate)
        self.lyt_interval.addWidget(self.lbl_recovery_duration)

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

        # Adding title bar.
        lbl_index = QLabel('Index')
        lbl_index.setFont(QFont('Bahnschrift Semibold', 15))
        lbl_speed_heart_rate = QLabel('Speed HR')
        lbl_speed_heart_rate.setFont(QFont('Bahnschrift Semibold', 15))
        lbl_speed_duration = QLabel('Speed time')
        lbl_speed_duration.setFont(QFont('Bahnschrift Semibold', 15))
        lbl_recovery_heart_rate = QLabel('Rest HR')
        lbl_recovery_heart_rate.setFont(QFont('Bahnschrift Semibold', 15))
        lbl_recovery_duration = QLabel('Rest time')
        lbl_recovery_duration.setFont(QFont('Bahnschrift Semibold', 15))
        lyt_title = QHBoxLayout()
        lyt_title.addWidget(lbl_index)
        lyt_title.addWidget(lbl_speed_heart_rate)
        lyt_title.addWidget(lbl_speed_duration)
        lyt_title.addWidget(lbl_recovery_heart_rate)
        lyt_title.addWidget(lbl_recovery_duration)
        lyt_training_intervals.addLayout(lyt_title)

        index = 1
        for interval in intervals:
            interval.render(index)
            lyt_training_intervals.addLayout(interval.lyt_interval)
            index += 1

        return lyt_training_intervals
