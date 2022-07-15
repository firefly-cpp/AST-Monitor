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
from PyQt5.QtWidgets import QLabel, QMessageBox
from threading import Thread

from ast_monitor.classes import Interval, SensorData
from ast_monitor.digital_twin import DigitalTwin
from ast_monitor.mainwindow import Ui_MainWindow
from ast_monitor.send_data import SendData


TICK_TIME = 1000


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
        self.planned_intervals = []
        self.intervals = []

        # Current interval data.
        self.current_interval = 0
        self.is_speed_phase = False
        self.interval_average_heart_rate = self.return_current_hr()
        self.interval_checkpoints = 0

        #
        self.training_timer = QTimer()

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

        # Show data in real time.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

        # Show interval data in real time.
        self.interval_timer = QTimer()
        self.interval_timer.timeout.connect(self.update_interval_data)
        self.interval_timer.start(1000)

        # Shutdown the computer.
        self.btn_shutdown.clicked.connect(self.shutdown_now)

        # On clicked buttons.
        self.tracker = QTimer()
        self.tracker.setInterval(TICK_TIME)
        self.tracker.timeout.connect(self.tick)
        self.do_reset()

        # Interval tick.
        self.interval_tracker = QTimer()
        self.interval_tracker.setInterval(TICK_TIME)
        self.interval_tracker.timeout.connect(self.interval_tick)
        self.do_interval_reset()

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
        self.interval_flag = False

        # Training button.
        self.btn_load_training.clicked.connect(self.load_training)
        self.btn_start_training.clicked.connect(self.start_training)

    def start_tracker(self, show_feedback: bool = True) -> None:
        """
        Start of the workout tracking.\n
        Args:
            show_feedback (bool):
                showing notification for workout start if True
        """
        self.tracker.start()
        self.tracking_flag = True

        self.widget_start_stop.setCurrentIndex(1)

        # Show simple notification that workout just started.
        if show_feedback:
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
        self.update_current_heart_rate(label=self.lbl_heart_rate)
        self.update_speed(label=self.lbl_speed)

        # Build_time_series in case tracker is enabled.
        if self.tracking_flag:
            self.build_time_series(series=self.time_series)
            self.update_distance(label=self.lbl_distance)

    @pyqtSlot()
    def update_interval_data(self) -> None:
        """
        Rendering all the necessary interval data.
        """
        # Build_time_series in case tracker is enabled.
        if self.interval_flag:
            self.update_current_heart_rate(label=self.lbl_interval_heart_rate)
            self.update_average_heart_rate(
                self.interval_average_heart_rate,
                self.return_current_hr(),
                label=self.lbl_interval_average_heart_rate
            )

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

    @pyqtSlot()
    def do_interval_reset(self) -> None:
        """
        Reset of the interval.
        """
        self.interval_time = 0

    def tick(self) -> None:
        """
        Incrementing time and displaying it on the stopwatch on each tick.
        """
        self.track_time += TICK_TIME / 1000
        self.display_stopwatch()

    def interval_tick(self) -> None:
        """
        Incrementing time and displaying it on
        the interval stopwatch on each tick.
        """
        self.interval_time += TICK_TIME / 1000
        self.display_interval_stopwatch()

        try:
            if self.digital_twin:
                self.digital_twin.current_heart_rate = self.return_current_hr()
                self.digital_twin.current_duration = self.interval_time
                
                if self.is_speed_phase:
                    diff = str(
                        '%+d' %
                        (self.return_current_hr() -
                         self.digital_twin.predicted_heart_rate)
                    )
                else:
                    diff = str(
                        '%+d' %
                        (self.digital_twin.predicted_heart_rate -
                         self.return_current_hr())
                    )

                if (
                    self.digital_twin.predicted_heart_rate >
                    self.digital_twin.current_heart_rate
                ):
                    self.swgt_interval_performance.setCurrentIndex(1)
                    self.lbl_interval_proposed_heart_rate.setText(
                        str(self.digital_twin.predicted_heart_rate)
                    )
                    self.lbl_interval_performance_up.setText(diff)
                else:
                    self.swgt_interval_performance.setCurrentIndex(2)
                    self.lbl_interval_proposed_heart_rate.setText(
                        str(self.digital_twin.predicted_heart_rate)
                    )
                    self.lbl_interval_performance_down.setText(diff)
        except Exception:
            pass

    def convert_time_to_hours_minutes_seconds(self, time: int) -> str:
        """
        Converting time in seconds to HH:MM:SS format.\n
        Args:
            time (int):
                time in seconds
        Returns:
            str: time in HH:MM:SS format
        """
        seconds = int(time % 60)
        minutes = int(time / 60)
        hours = int(minutes / 60)

        time = (
            str(hours) +
            ':' +
            (str(minutes) if minutes > 9 else '0' + str(minutes)) +
            ':' +
            (str(seconds) if seconds > 9 else '0' + str(seconds))
        )

        return time

    def display_stopwatch(self) -> None:
        """
        Displaying the stopwatch in the GUI.
        """
        time = self.convert_time_to_hours_minutes_seconds(self.track_time)
        self.lbl_watch.setText(time)

    def display_interval_stopwatch(self) -> None:
        """
        Displaying the stopwatch in the GUI.
        """
        time = self.convert_time_to_hours_minutes_seconds(self.interval_time)
        self.lbl_interval_watch.setText(time)

    def update_current_heart_rate(self, label: QLabel) -> None:
        """
        Calculating and displaying current heart rate.\n
        Args:
            label (QLabel):
                label to be updated
        """
        hr = self.return_current_hr()
        label.setText(str(hr))

    def update_average_heart_rate(
        self,
        previous_heart_rate: int,
        current_heart_rate: int,
        label: QLabel
    ) -> None:
        """
        Calculating and displaying average heart rate
        with a help of a recursive function.\n
        Args:
            previous_heart_rate (int):
                previous average heart rate
            current_heart_rate (int):
                current heart rate
            label (QLabel):
                label to be updated
        """
        if previous_heart_rate == -1:
            return
        elif previous_heart_rate == 0:
            average_heart_rate = current_heart_rate
        else:
            n = self.interval_checkpoints
            avg_hr = previous_heart_rate
            hr = current_heart_rate
            average_heart_rate = avg_hr + ((1 / n) * (hr - avg_hr))

        label.setText(str(int(average_heart_rate)))
        self.interval_average_heart_rate = average_heart_rate
        self.interval_checkpoints += 1

    def update_speed(self, label: QLabel) -> None:
        """
        Calculating and displaying current speed.\n
        Args:
            label (QLabel):
                label to be updated
        """
        speed = self.calculate_speed()
        label.setText(f'{speed} km/h')

    def update_distance(self, label: QLabel) -> None:
        """
        Calculating and displaying distance.\n
        Args:
            label (QLabel):
                label to be updated
        """
        dist = self.calculate_distance(self.time_series)

        # If there is no distance made yet, 0.00 km is displayed.
        if not dist:
            label.setText('0.00 km')
        else:
            rounded_dist = round(dist, 2)
            dist_str = '{:.2f}'.format(rounded_dist / 1000)
            label.setText(dist_str + ' km')

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

    def build_time_series(self, series: list) -> None:
        """
        Building time series from the collected
        GPS data, HR data and current time.\n
        Args:
            series (list[SensorData]):
                list of series
        """
        HR = self.return_current_hr()
        GPS_LON, GPS_LAT, GPS_ALT = self.return_current_gps()
        TIME = self.get_current_timestamp()
        DIST = self.calculate_distance(series)
        series.append(
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

    def calculate_distance(self, series: list) -> float:
        """
        Calculate distance of the workout.\n
        Args:
            series (list[SensorData])
        Returns:
            float: total distance
        """
        if (len(series) < 2):
            return 0.0

        total_distance = 0.0
        for i in range(len(series) - 1):
            coords_1 = (
                series[i + 1].longitude,
                series[i + 1].latitude
            )
            coords_2 = (
                series[i].longitude,
                series[i].latitude
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

    def start_training(self) -> None:
        """
        Manual training start.
        """
        i = self.current_interval

        if i == 0:
            self.start_tracker(show_feedback=False)
        elif i >= len(self.planned_intervals):
            self.end_tracker()
            return

        self.start_interval_speed()

        self.training_timer = QTimer()
        self.training_timer.timeout.connect(self.end_interval_speed)
        self.training_timer.start(
            60 * 1000 * self.planned_intervals[i].speed_duration
        )

        self.current_interval += 1

    def start_interval_speed(self):
        """
        Starting a speed part of an interval.
        """
        self.interval_tracker.start()
        self.interval_flag = True
        self.interval_average_heart_rate = 0
        self.interval_duration = 0
        self.interval_time = 0.0
        self.is_speed_phase = True
        self.lbl_interval_proposed_heart_rate.setText('-')

        # Launching the digital twin.
        interval = self.planned_intervals[self.current_interval]
        self.digital_twin = DigitalTwin(
            interval.speed_heart_rate,
            interval.speed_duration,
            TICK_TIME
        )
        self.digital_twin_thread = Thread(
            target=self.digital_twin.predict_heart_rate
        )
        self.digital_twin_thread.start()

        # Show simple notification that an interval just started.
        self._feedback = TextFeedback(text='Interval started!')
        self._feedback.show(
            AnimationType.HORIZONTAL,
            AnimationDirection.RIGHT,
            time=3000
        )

    def end_interval_speed(self):
        """
        Ending a speed part of an interval.
        """
        self.interval_time = 0.0
        self.interval_average_heart_rate = 0
        self.interval_checkpoints = 0
        self.lbl_interval_average_heart_rate.setText('-')
        self.lbl_interval_proposed_heart_rate.setText('-')
        self.is_speed_phase = False
        self.swgt_interval_performance.setCurrentIndex(0)

        self.start_interval_rest()

    def start_interval_rest(self):
        """
        Starting a rest part of an interval.
        """
        self.lbl_interval_watch.setText('0:00:00')
        self.lbl_interval_proposed_heart_rate.setText('-')
        self.interval_checkpoints = 1
        self.interval_average_heart_rate = self.return_current_hr()

        # Show simple notification that an interval just started.
        self._feedback = TextFeedback(text='Rest started!')
        self._feedback.show(
            AnimationType.HORIZONTAL,
            AnimationDirection.RIGHT,
            time=3000
        )

        interval = self.planned_intervals[self.current_interval]
        self.training_timer = QTimer()
        self.training_timer.timeout.connect(self.end_interval_rest)
        self.training_timer.start(
            60 * 1000 * interval.recovery_duration
        )

        # Launching the digital twin.
        del self.digital_twin
        self.digital_twin = DigitalTwin(
            interval.recovery_heart_rate,
            interval.recovery_duration,
            TICK_TIME
        )
        self.digital_twin_thread = Thread(
            target=self.digital_twin.predict_heart_rate
        )
        self.digital_twin_thread.start()

    def end_interval_rest(self):
        """
        Ending a rest part of an interval.
        """
        self.interval_time = 0.0
        self.interval_average_heart_rate = 0
        self.interval_checkpoints = 0
        self.lbl_interval_average_heart_rate.setText('-')
        self.lbl_interval_proposed_heart_rate.setText('-')
        self.swgt_interval_performance.setCurrentIndex(0)
        self.training_timer.stop()

        self.start_training()

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
            Interval.render_intervals(self.planned_intervals)
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
        self.planned_intervals = []
        for interval_group in training['interval']:
            for i in range(interval_group['repetitions']):
                interval = Interval(
                    interval_group['speed_duration'],
                    interval_group['recovery_duration'],
                    interval_group['speed_heart_rate'],
                    interval_group['recovery_heart_rate']
                )
                self.planned_intervals.append(interval)

        # self.intervals = list(map(lambda i: i, training['interval']))
        self.render_intervals_GUI()
