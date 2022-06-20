from datetime import datetime
import geopy.distance
import json
import os
from pyqt_feedback_flow.feedback import (
    AnimationDirection,
    AnimationType,
    TextFeedback
)
from PyQt5 import (
    QtCore,
    QtWidgets,
    QtWebChannel,
    QtWebEngineWidgets
)
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtWidgets import QMessageBox

from ast_monitor.classes import Interval, SensorData
from ast_monitor.mainwindow import Ui_MainWindow
from ast_monitor.send_data import SendData


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
        self.initialize_GUI()  # GUI initialization.

        # Paths to heart rate and GPS data files.
        self.hr_data_path = hr_data_path
        self.gps_data_path = gps_data_path

        # Structures for storing data and intervals.
        self.time_series = []
        self.intervals = []

    def initialize_GUI(self) -> None:
        """
        Initialization of the AST-Monitor GUI.
        """
        QtWidgets.QMainWindow.__init__(self, flags=Qt.FramelessWindowHint)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Map setting.
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("MainWindow", self)
        self.view.page().setWebChannel(self.channel)
        file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../ast_monitor/map/map.html',
        )
        self.view.setUrl(QtCore.QUrl.fromLocalFile(file))
        self.vb_map.addWidget(self.view)

        # Show HR in real time.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

        # Shutdown the computer.
        self.btn_shutdown.clicked.connect(self.shutdown_now)

        # On clicked buttons.
        self.tracker = QTimer()
        self.tracker.setInterval(TICK_TIME)
        self.tracker.timeout.connect(self.tick)
        self.do_reset()

        # Menu buttons.
        self.action_about_program.triggered.connect(self.about)
        self.action_license.triggered.connect(self.license)
        self.action_disclaimer.triggered.connect(self.disclaimer)

        # Tracking buttons.
        self.tracking_flag = False
        self.btn_start_tracking.clicked.connect(self.start_tracker)
        self.btn_stop_tracking.clicked.connect(self.end_tracker)

        # Left and right menu buttons.
        self.btn_move_left.clicked.connect(self.menu_left_move)
        self.btn_move_right.clicked.connect(self.menu_right_move)

        # Interval buttons.
        self.btn_start_interval.clicked.connect(self.start_interval)
        self.btn_end_interval.clicked.connect(self.end_interval)

        # Training button.
        self.btn_load_training.clicked.connect(self.load_training)

    def start_tracker(self) -> None:
        """
        Start of the workout tracking.
        """
        self.tracker.start()
        self.tracking_flag = True

        self.widget_start_stop.setCurrentIndex(1)

        # Sending data in real time.
        self.timer_data = QTimer()
        self.timer_data.timeout.connect(self.send_data)
        self.timer_data.start(10000)

        # Show simple notification that workout just started.
        self._feedback = TextFeedback(text='Workout started!')
        self._feedback.show(
            AnimationType.VERTICAL,
            AnimationDirection.UP,
            time=3000
        )

    def end_tracker(self) -> None:
        """
        End of the workout tracking.
        """
        self.tracker.stop()
        self.tracking_flag = False

        self.widget_start_stop.setCurrentIndex(0)

        # Show simple notification that workout just enden.
        self._feedback = TextFeedback(text='Workout ended!')
        self._feedback.show(
            AnimationType.VERTICAL,
            AnimationDirection.DOWN,
            time=3000
        )

    @pyqtSlot()
    def update_data(self) -> None:
        """
        Rendering all the necessary data.
        """
        self.update_hr()
        self.update_speed()

        # Build_time_series in case tracker is enabled.
        if self.tracking_flag:
            self.build_time_series()
            self.update_distance()

    @pyqtSlot()
    def send_data(self) -> None:
        """
        Sending the training data to the API.
        """
        SendData.send_data(self.time_series)

    @pyqtSlot()
    def do_reset(self) -> None:
        """
        Reset of the stopwatch.
        """
        self.track_time = 0
        self.display_stopwatch()

    def tick(self) -> None:
        """
        Incrementing time and displaying it on the stopwatch on each tick.
        """
        self.track_time += TICK_TIME / 1000
        self.display_stopwatch()

    def display_stopwatch(self) -> None:
        """
        Displaying the stopwatch in GUI.
        """
        seconds = int(self.track_time % 60)
        minutes = int(self.track_time / 60)
        hours = int(minutes / 60)

        time = (
            str(hours) +
            ':' +
            (str(minutes) if minutes > 9 else '0' + str(minutes)) +
            ':' +
            (str(seconds) if seconds > 9 else '0' + str(seconds))
        )

        self.lbl_watch.setText(time)

    def update_distance(self) -> None:
        """
        Calculating and displaying distance.
        """
        dist = self.calculate_distance()

        # If there is no distance made yet, 0.00 km is displayed.
        if not dist:
            self.lbl_distance.setText('0.00 km')
        else:
            rounded_dist = round(dist, 2)
            dist_str = '{:.2f}'.format(rounded_dist / 1000)
            self.lbl_distance.setText(dist_str + ' km')

    def update_speed(self) -> None:
        """
        Calculating and updating speed.
        """
        speed = self.calculate_speed()
        self.lbl_speed.setText(f'{speed} km/h')

    def update_ascent(self) -> None:
        """
        Calculating and updating ascent.
        """
        pass

    def update_hr(self) -> None:
        """
        Calculating and displaying average heart rate.
        """
        hr = self.return_current_hr()
        self.lbl_heart_rate.setText(str(hr))

    def update_interval_hr(self) -> None:
        """
        Calculating and displaying interval heart rate.
        """
        pass

    def shutdown_now(self) -> None:
        """
        Shutdown of the system.
        """
        os.system('shutdown now -h')

    def get_current_time(self) -> str:
        """
        Getting current time as string.\n
        Returns:
            str: current time (HH:MM:SS)
        """
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        return current_time

    def get_current_timestamp(self) -> datetime:
        """
        Getting current time as datetime.\n
        Returns:
            datetime: current datetime
        """
        now = datetime.now()
        return now

    def build_time_series(self) -> None:
        """
        Building time series from the collected
        GPS data, HR data and current time.
        """
        HR = self.return_current_hr()
        GPS_LON, GPS_LAT, GPS_ALT = self.return_current_gps()
        TIME = self.get_current_time()
        DIST = self.calculate_distance()
        self.time_series.append(
            SensorData(HR, GPS_LON, GPS_LAT, GPS_ALT, TIME, DIST)
        )

    def return_current_hr(self) -> int:
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
            self.calculate_average_heart_rate(array)
            final = str(array[-1])

        return int(final)

    def return_current_gps(self) -> tuple:
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

    def calculate_average_heart_rate(self, hr_data: list) -> float:
        """
        Calculate average HR of the workout.\n
        Args:
            hr_data (list):
                a list of all HR values of the workout
        Returns:
            float: average heart rate of the workout
        """
        av_hr = sum(hr_data) / len(hr_data)
        return av_hr

    def calculate_distance(self) -> float:
        """
        Calculate distance of workout.\n
        Returns:
            float: total distance
        """
        if (len(self.time_series) < 2):
            return 0.0

        total_distance = 0.0
        for i in range(len(self.time_series) - 1):
            coords_1 = (
                self.time_series[i + 1].longitude,
                self.time_series[i + 1].latitude
            )
            coords_2 = (
                self.time_series[i].longitude,
                self.time_series[i].latitude
            )
            total_distance = (
                total_distance +
                abs(geopy.distance.geodesic(coords_1, coords_2).m)
            )

        return round(total_distance, 3)

    def calculate_speed(self) -> float:
        """
        Speed calculation in km/h.\n
        Returns:
            float: current speed in km/h
        """
        if len(self.time_series) < 2:
            return 0.0

        prev_stamp = self.time_series[-2]
        cur_stamp = self.time_series[-1]
        speed = (
            3.6 *
            (cur_stamp.distance - prev_stamp.distance) /
            (cur_stamp.time - prev_stamp.time).total_seconds()
        )
        return round(speed, 1)

    def about(self) -> None:
        """
        Show information about application.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Developed by I. Fister Jr., L. Lukač, 2022')
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

    def disclaimer(self) -> None:
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

    def menu_left_move(self) -> None:
        """
        Moving left in the menu.
        """
        index = self.stackedWidget.currentIndex()
        if index == 0:
            return

        self.stackedWidget.setCurrentIndex(index - 1)
        self.widget_title.setCurrentIndex(index - 1)

    def menu_right_move(self) -> None:
        """
        Moving right in the menu.
        """
        index = self.stackedWidget.currentIndex()
        if index == self.stackedWidget.count():
            return

        self.stackedWidget.setCurrentIndex(index + 1)
        self.widget_title.setCurrentIndex(index + 1)

    def start_interval(self) -> None:
        """
        Manual interval start.
        """
        self.widget_interval_button.setCurrentIndex(1)

        # Show simple notification that an interval just started.
        self._feedback = TextFeedback(text='Interval started!')
        self._feedback.show(
            AnimationType.HORIZONTAL,
            AnimationDirection.RIGHT,
            time=3000
        )

    def end_interval(self) -> None:
        """
        Manual interval end.
        """
        self.widget_interval_button.setCurrentIndex(0)

        # Show simple notification that an interval just ended.
        self._feedback = TextFeedback(text='Interval ended!')
        self._feedback.show(
            AnimationType.HORIZONTAL,
            AnimationDirection.LEFT,
            time=3000
        )

    def render_intervals_GUI(self) -> None:
        """
        Rendering the read intervals in the GUI.
        """
        # Removing old intervals or text.
        if self.lbl_no_training:
            self.lbl_no_training.deleteLater()
            self.lbl_no_training = None
        old_intervals = self.lyt_training.takeAt(0)
        self.lyt_training.removeItem(old_intervals)

        # Inserting the read intervals.
        self.lyt_training.insertLayout(
            0,
            Interval.render_intervals(self.intervals)
        )

    def load_training(self) -> None:
        """
        Loading training from JSON file.\n
        Args:
            file (str):
                path to the file
        """
        # Currently hard-coded path to the file.
        file = '../development/trainings/training.json'

        # Opening and reading the training data.
        training = {}
        with open(file, 'r') as f:
            training_json = f.read()
            training = json.loads(training_json)

        # Displaying a notification about training load.
        self._feedback = TextFeedback(text='Training loaded successfully')
        self._feedback.show(
            AnimationType.HORIZONTAL,
            AnimationDirection.RIGHT,
            time=3000
        )

        # Adding and rendering the intervals from the training.
        self.intervals = list(map(lambda i: i, training['interval']))
        self.render_intervals_GUI()
