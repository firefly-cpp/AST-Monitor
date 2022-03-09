from datetime import datetime
import geopy.distance
import os
from pyqt_feedback_flow.feedback import (
    AnimationDirection,
    AnimationType,
    TextFeedback
)
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QDateTime, QTimer
from PyQt5.QtWidgets import QMessageBox

from ast_monitor.classes import SensorData
from ast_monitor.mainwindow import Ui_MainWindow


TICK_TIME = 2**6


class AST(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main class that represents the interface between computer and athlete.\n
    Args:
        hr_data_path (str):
            path to file for storing HR data
        gps_path (str):
            path to file for storing GPS data
    """

    def __init__(self, hr_data_path: str, gps_data_path: str) -> None:
        """
        Initialisation method for AST class.\n
        Args:
            hr_data_path (str):
                path to file for storing HR data
            gps_path (str):
                path to file for storing GPS data
        """
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.hr_data_path = hr_data_path
        self.gps_data_path = gps_data_path
        self.time_series = []  # Storing all the data in this struct
        self.hr_data_collection = []

        # Show HR in real time.
        self.timer = QTimer()
        self.timer.timeout.connect(self.real_time_hr)
        self.timer.start(1000)

        # Taking values from the sensors.
        # self.build_time_series()

        # Shutdown the computer.
        self.shutdown.clicked.connect(self.shutdown_now)

        # On clicked buttons.
        self.tracker = QTimer()
        self.tracker.setInterval(TICK_TIME)
        self.tracker.timeout.connect(self.tick)
        self.do_reset()

        # Menu buttons.
        self.actionAbout_program.triggered.connect(self.about)
        self.actionLicense.triggered.connect(self.license)
        self.actionDisclaimer.triggered.connect(self.disclaimer)

        self.tracking_flag = False
        self.start_tracking.clicked.connect(self.startTracking)

        self.stop_tracking.clicked.connect(self.endTracker)

    def startTracking(self) -> None:
        """
        Start tracker for tracking the workout.
        """
        self.startTracker()
        self.tracking_flag = True

        # Show simple notification that workout just started.
        self._feedback = TextFeedback(text='Workout started!')
        self._feedback.show(
            AnimationType.VERTICAL,
            AnimationDirection.UP,
            time=3000
        )

    def startTracker(self) -> None:
        """
        Starting tracker.
        """
        self.tracker.start()

    def endTracker(self) -> None:
        """
        Ending tracker.
        """
        self.tracker.stop()
        self.tracking_flag = False

    def tick(self) -> None:
        """
        Incrementing time and displaying it on the stopwatch on each tick.
        """
        self.track_time += TICK_TIME / 1000
        self.display_stopwatch()

    def display_stopwatch(self) -> None:
        """
        Displaying the stopwatch.
        """
        self.watch.display(
            '%d:%05.2f'
            % (self.track_time // 60, self.track_time % 60)
        )

    def update_distance(self) -> None:
        """
        Calculating and displaying distance.
        """
        dist = self.calculate_distance()
        
        # If there is no distance made yet, 0 is displayed.
        if not dist:
            self.total_distance.setText('0.00 km')
        else:
            rounded_dist = round(dist, 2)
            dist_str = '{:.2f}'.format(rounded_dist)
            self.total_distance.setText(dist_str + ' km')

    def update_ascent(self) -> None:
        """
        Calculating and updating ascent.
        """
        pass

    def update_average_hr(self) -> None:
        """
        Calculating and displaying average heart rate.
        """
        avhr = str(self.calculate_avhr())
        self.average_hr.setText(avhr)

    def update_interval_hr(self) -> None:
        """
        Calculating and displaying interval heart rate.
        """
        pass

    @pyqtSlot()
    def do_reset(self) -> None:
        """
        Reset of the stopwatch.
        """
        self.track_time = 0
        self.display_stopwatch()

    def showtrackingTime(self) -> None:
        """
        Displaying tracking time.
        """
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.label.setText(timeDisplay)

    def shutdown_now(self) -> None:
        """
        Shutdown of the system.
        """
        os.system('shutdown now -h')

    def startTimer(self) -> None:
        """
        Starting timer.
        """
        self.timer.start(1000)

    def endTimer(self) -> None:
        """
        Ending timer.
        """
        self.timer.stop()

    def get_current_time(self) -> datetime:
        """
        Getting current time.\n
        Returns:
            datetime: current time
        """
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        return current_time

    def build_time_series(self) -> None:
        """
        Build time series from the collected
        GPS data, HR data and current time.
        """
        HR = self.return_curr_hr()
        GPS_LON, GPS_LAT, GPS_ALT = self.return_curr_gps()
        TIME = self.get_current_time
        self.time_series.append(
            SensorData(
                HR,
                GPS_LON,
                GPS_LAT,
                GPS_ALT,
                TIME
            )
        )

    @pyqtSlot()
    def real_time_hr(self) -> int:
        """
        Show current HR value.\n
        Returns:
            int: current heart rate
        """
        hr_val = self.return_curr_hr()
        self.current_hr.setText(str(hr_val))

        # Build_time_series in case tracker is enabled.
        if self.tracking_flag:
            self.build_time_series()
            self.update_distance()
            # self.update_average_hr()

        return int(hr_val)

    def return_curr_hr(self) -> int:
        """
        Get current HR data from file.\n
        Returns:
            int: current heart rate
        """
        # If file is empty.
        # Note: should be improved.
        if os.stat(self.hr_data_path).st_size == 0:
            return 0

        with open(self.hr_data_path, 'r') as ins:
            array = []
            for line in ins:
                array.append(int(line.rstrip()))

            # Use data for calculation of average HR.
            self.calculate_avhr(array)
            final = str(array[-1])

        return int(final)

    def return_curr_gps(self) -> tuple:
        """
        Get current GPS data from file.\n
        Returns:
            tuple(float, float, float):
        """
        # If file is empty.
        # Note: should be improved.
        if os.stat(self.gps_data_path).st_size == 0:
            return 0.0, 0.0, 0.0

        with open(self.gps_data_path, 'r') as ins:
            array = []
            for line in ins:
                array.append(line)

            final1 = str(array[-1].rstrip())
            final = final1.split(";")

        return float(final[0]), float(final[1]), float(final[2])

    def calculate_avhr(self, hr_data: list) -> float:
        """
        Calculate average HR of the workout.\n
        Args:
            hr_data (list):
                a list of all HR values of the workout
        Returns:
            float: average heart rate of the workout
        """
        avhr = sum(hr_data) / len(hr_data)
        return avhr

    def calculate_distance(self) -> float:
        """
        Calculate distance of workout.\n
        Returns:
            float: total distance
        """
        total_distance = 0.0
        if (len(self.time_series) < 5):
            pass
        else:
            for i in range(len(self.time_series) - 1):
                coords_1 = (self.time_series[i + 1].lon,
                            self.time_series[i + 1].lat)
                coords_2 = (self.time_series[i].lon, self.time_series[i].lat)
                total_distance = total_distance + \
                    abs(geopy.distance.geodesic(coords_1, coords_2).m)

            return round((total_distance / 1000), 3)

    def about(self) -> None:
        """
        Show information about application.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Developed by I. Fister Jr., 2021')
        msg.setWindowTitle('About this application')
        msg.exec_()

    def license(self) -> None:
        """
        Show license information.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Licensed under MIT license!')
        msg.setWindowTitle('License info!')
        msg.exec_()

    def disclaimer(self):
        """
        Show disclaimer info.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Disclaimer')
        msg.setDetailedText(
            'This framework is provided as-is, and there are no guarantees '
            'that it fits your purposes or that it is bug-free. Use it at '
            'your own risk!')
        msg.exec_()
