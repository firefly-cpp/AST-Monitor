import glob
import json
import os
import socketserver

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtCore import pyqtSlot, Qt, QTimer, QUrl
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWidgets import QMainWindow

from ast_monitor.goals_processor import GoalsProcessor
from ast_monitor.html_request_handler import CustomHandler
from ast_monitor.route_reader import RouteReader

try:
    from PyQt6.QtWebChannel import QWebChannel
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except Exception:
    pass
from pyqt_feedback_flow.feedback import (
    AnimationDirection,
    AnimationType,
    TextFeedback
)
import threading
import time

from ast_monitor.basic_data import BasicData
from ast_monitor.interval_training import IntervalTraining
from ast_monitor.mainwindow import Ui_MainWindow
from ast_monitor.training_session import TrainingSession


class AST(QMainWindow, Ui_MainWindow):
    """
    Main class for the manipulation with the GUI of the application.\n
    Args:
        hr_data_path (str):
            path to the file that contains heart rate data
        gps_data_path (str):
            path to the file that contains GPS data
    """

    def __init__(self, hr_data_path: str, gps_data_path: str, route_data_path=None) -> None:
        """
        Initialization method for AST class.\n
        Args:
            hr_data_path (str):
                path to the file that contains heart rate data
            gps_data_path (str):
                path to the file that contains GPS data
            route_dict (dict):
                dictionary with route data
        """
        if route_data_path is None:
            self.route = None
        else:
            rr = RouteReader(route_data_path)
            self.route = rr.read()

        self.basic_data = BasicData(hr_data_path, gps_data_path)
        self.initialize_GUI()
        self.map_initialized = False
        self.goals_processor = None

        self.server_thread = HttpServerThread()
        self.server_thread.start()

    def on_load_finished(self):
        self.map_initialized = True
        if self.route is not None:
            self.goals_processor = GoalsProcessor(self.route)
            self.update_map_component(
                route_input=self.route
            )

    def initialize_GUI(self) -> None:
        """
        Initialization method for the GUI of the app.
        """
        QMainWindow.__init__(self, flags=Qt.WindowType.FramelessWindowHint)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Map setting (not working on Raspberry Pi
        # OS due to missing dependencies).
        try:
            self.view = QWebEngineView()
            self.view.settings().setAttribute(
                QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
            self.view.settings().setAttribute(
                QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
            self.channel = QWebChannel()
            self.channel.registerObject("MainWindow", self)
            self.view.page().setWebChannel(self.channel)

            self.view.setUrl(QUrl("http://localhost:8000"))
            self.view.loadFinished.connect(self.on_load_finished)

            self.vb_map.addWidget(self.view)
        except NameError:
            print('No QtWebEngine module found.')

        # Shutdown of the computer.
        self.btn_shutdown.clicked.connect(self.shutdown)

        # Connecting slots for the start and the end of the training session.
        self.btn_start_tracking.clicked.connect(self.start_training_session)
        self.btn_stop_tracking.clicked.connect(self.end_training_session)

        # Connecting slots for moving inside the main menu.
        self.btn_move_left.clicked.connect(self.menu_left)
        self.btn_move_right.clicked.connect(self.menu_right)

        # Connecting slots for loading and starting an interval training.
        self.btn_load_training.clicked.connect(self.load_training)
        self.btn_start_training.clicked.connect(self.start_training)

        # Rendering data in the GUI of the app.
        self.timer = QTimer()
        self.timer.timeout.connect(self.render_data)
        self.timer.start(250)

    def update_map_component(self, progress: float = None, remaining_distance: float = None,
                             remaining_ascent: float = None, speed: float = None,
                             heartrate: int = None, duration=None, distance=None,
                             lat_lng=None, ascent=None, route_input=None):
        """
        Updating method for the (Vue.js rendered) map component with the new data.
        Args:
            progress (float):
            remaining_distance (float):
            remaining_ascent (float):
            speed (float):
            heartrate (int):
            duration:
            distance:
            lat_lng:
            ascent:
            route_input:

        Returns:

        """
        js_call = "setValues({"

        if progress is not None:
            js_call += f"progress: {progress},"
        if remaining_distance is not None:
            js_call += f"remainingDistance: {remaining_distance},"
        if remaining_ascent is not None:
            js_call += f"remainingAscent: {remaining_ascent},"
        if speed is not None:
            js_call += f"speed: {speed},"
        if heartrate is not None:
            js_call += f"heartrate: {heartrate},"
        if duration is not None:
            js_call += f"duration: '{duration}',"
        if distance is not None:
            js_call += f"distance: {distance},"
        if lat_lng is not None:
            js_call += f"lat_lng: [{lat_lng[0]}, {lat_lng[1]}],"
        if ascent is not None:
            js_call += f"ascent: {ascent},"
        if route_input is not None:
            js_call += f"routeInput: {route_input['route_render']},"
        js_call += "});"
        self.view.page().runJavaScript(js_call)

    @pyqtSlot()
    def shutdown(self) -> None:
        """
        Shutdown of AST-Monitor.
        """
        os.system('shutdown now -h')

    @pyqtSlot()
    def start_training_session(self, show_feedback: bool = True) -> None:
        """
        Start of the training session.\n
        Args:
            show_feedback (bool):
                if True, show notification for starting a training session
        """
        self.session = TrainingSession()
        self.widget_start_stop.setCurrentIndex(1)

        # Show simple notification that session just started.
        if show_feedback:
            feedback = TextFeedback(text='Training session started!')
            feedback.show(
                AnimationType.VERTICAL,
                AnimationDirection.UP,
                time=3000
            )

    @pyqtSlot()
    def end_training_session(self, show_feedback: bool = True) -> None:
        """
        End of the training session.\n
        Args:
            show_feedback (bool):
                if True, show notification for ending a training session
        """
        del self.session
        self.widget_start_stop.setCurrentIndex(0)

        if hasattr(self, 'interval_training'):
            self.interval_training.abort_training = True

        # Show simple notification that session just ended.
        if show_feedback:
            self._feedback = TextFeedback(text='Training session ended!')
            self._feedback.show(
                AnimationType.VERTICAL,
                AnimationDirection.DOWN,
                time=3000
            )

    @pyqtSlot()
    def menu_left(self) -> None:
        """
        Move to the left in the main menu.
        """
        index = self.stackedWidget.currentIndex()
        if index == 0:
            return

        self.stackedWidget.setCurrentIndex(index - 1)
        self.widget_title.setCurrentIndex(index - 1)

    @pyqtSlot()
    def menu_right(self) -> None:
        """
        Move to the right in the main menu.
        """
        index = self.stackedWidget.currentIndex()
        if index == self.stackedWidget.count():
            return

        self.stackedWidget.setCurrentIndex(index + 1)
        self.widget_title.setCurrentIndex(index + 1)

    @pyqtSlot()
    def load_training(self, show_feedback: bool = True) -> None:
        """
        Loading an interval training from a JSON file.
        Args:
            show_feedback (bool):
                if True, show notification for successful training
        """
        # Getting all available trainings.
        trainings = glob.glob(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), '..', 'development', 'trainings', '*.json'))

        # Opening and reading the training data.
        name = ''
        for i in range(len(trainings)):
            with open(trainings[i], 'r') as f:
                training_json = f.read()
                training = json.loads(training_json)
                training['file'] = trainings[i].split('\\')[-1]
                try:
                    interval_training = IntervalTraining(
                        training,
                        self.basic_data
                    )
                    if (
                            not hasattr(self, 'interval_training') or
                            not self.interval_training == interval_training
                    ):
                        self.interval_training = interval_training
                        name = trainings[i].split('\\')[-1].split('.')[0]
                        break
                except Exception:
                    pass
        else:
            with open(trainings[0], 'r') as f:
                training_json = f.read()
                training = json.loads(training_json)
                training['file'] = trainings[0].split('\\')[-1].split('.')[0]
                name = trainings[i].split('\\')[-1].split('.')[0]
                self.interval_training = IntervalTraining(
                    training,
                    self.basic_data
                )

        # Adding and rendering the intervals from the training.
        self.widget_training_data.setCurrentIndex(1)
        self.lbl_training_file.setText(name)
        self.lbl_training_type.setText('Interval')
        self.lbl_training_speed_duration.setText(
            f'{str(self.interval_training.speed_duration)} min'
        )
        self.lbl_training_speed_hr.setText(
            str(self.interval_training.speed_heart_rate)
        )
        self.lbl_training_rest_duration.setText(
            f'{str(self.interval_training.recovery_duration)} min'
        )
        self.lbl_training_rest_hr.setText(
            str(self.interval_training.recovery_heart_rate)
        )
        self.lbl_training_repetitions.setText(
            str(self.interval_training.repetitions)
        )

        # Displaying a notification about the successful training loading.
        if show_feedback:
            self._feedback = TextFeedback(text='Training loaded successfully')
            self._feedback.show(
                AnimationType.HORIZONTAL,
                AnimationDirection.RIGHT,
                time=3000
            )

    @pyqtSlot()
    def start_training(self) -> None:
        """
        Start of the interval training.
        """
        if hasattr(self, 'interval_training'):
            self.stackedWidget.setCurrentIndex(2)
            self.widget_title.setCurrentIndex(2)
            self.interval_training.abort_training = False
            self.start_training_session(show_feedback=False)
            threading.Thread(
                target=lambda: self.interval_training.start(write_log=True)
            ).start()

    @pyqtSlot()
    def render_data(self) -> None:
        """
        Render method for the GUI of the app.
        """
        # Heart rate rendering.
        self.basic_data.read_current_hr()
        current_hr = self.basic_data.current_heart_rate
        if current_hr:
            self.lbl_heart_rate.setText(str(current_hr))
            self.update_map_component(heartrate=current_hr)
        else:
            self.lbl_heart_rate.setText('-')

        # Speed rendering.
        self.basic_data.read_current_gps()

        self.basic_data.calculate_speed()
        current_speed = self.basic_data.current_speed
        if current_speed is not None:
            self.lbl_speed.setText(f'{round(current_speed, 1)} km/h')
            self.update_map_component(speed=round(current_speed, 1))
        else:
            self.lbl_speed.setText('-')

        # Training session rendering.
        if hasattr(self, 'session'):
            # Session time rendering.
            self.session.calculate_time()
            time_s = self.convert_time_to_hours_minutes_seconds(
                int(self.session.time)
            )
            self.lbl_watch.setText(time_s)
            # Session distance rendering.
            self.session.add_distance(self.basic_data.distance)
            self.lbl_distance.setText(
                '{:.2f} km'.format(round(self.session.distance / 1000, 2))
            )
            self.update_map_component(distance=round(
                self.session.distance / 1000, 2), duration=time_s)

            # Total ascent rendering.
            if self.basic_data.current_gps:
                self.session.add_ascent(self.basic_data.current_gps[2])
                print(self.basic_data.current_gps[0:2])
                self.update_map_component(
                    lat_lng=self.basic_data.current_gps[0:2], ascent=int(self.session.ascent))
                if self.route is not None and self.basic_data.current_gps is not None:
                    self.goals_processor.add_position(
                        self.basic_data.current_gps)
                    gp: GoalsProcessor = self.goals_processor
                    self.update_map_component(progress=round(gp.progress * 100, 0),
                                              remaining_ascent=round(
                                                  gp.ascent_to_go, 1),
                                              remaining_distance=round(float(gp.distance_to_go / 1000), 1))
                self.lbl_ascent.setText(f'{int(self.session.ascent)} m')

        # Interval training rendering.
        if (
                hasattr(self, 'interval_training') and
                not self.interval_training.abort_training
        ):
            # Showing notifications.
            if self.interval_training.speed_notification:
                # Show simple notification that a speed interval just started.
                self.interval_training.speed_notification = False
                current = self.interval_training.current_interval[0] + 1
                total = self.interval_training.repetitions
                TextFeedback(f'{current}/{total}: Speed phase started!').show(
                    AnimationType.HORIZONTAL,
                    AnimationDirection.RIGHT,
                    time=3000
                )
            elif self.interval_training.recovery_notification:
                # Show simple notification that a
                # recovery interval just started.
                self.interval_training.recovery_notification = False
                current = self.interval_training.current_interval[0] + 1
                total = self.interval_training.repetitions
                TextFeedback(f'{current}/{total}: Rest phase started!').show(
                    AnimationType.HORIZONTAL,
                    AnimationDirection.RIGHT,
                    time=3000
                )

            # Interval time rendering (separate phase).
            if self.interval_training.phase_start:
                time_s = self.convert_time_to_hours_minutes_seconds(
                    int(time.time() - self.interval_training.phase_start)
                )
                self.lbl_interval_watch.setText(time_s)

            # Interval current heart rate rendering.
            if current_hr:
                self.lbl_interval_heart_rate.setText(str(current_hr))
            else:
                self.lbl_interval_heart_rate.setText('-')

            # Digital twin data rendering.
            if hasattr(self.interval_training, 'digital_twin'):
                digital_twin = self.interval_training.digital_twin

                # Digital twin prediction rendering.
                if hasattr(digital_twin, 'predicted_heart_rate'):
                    predicted_hr = digital_twin.predicted_heart_rate
                    if predicted_hr:
                        self.lbl_interval_proposed_heart_rate.setText(
                            str(predicted_hr)
                        )
                    else:
                        self.lbl_interval_proposed_heart_rate.setText('-')

                # Difference between digital twin prediction
                # and the current heart rate rendering.
                if hasattr(digital_twin, 'predicted_heart_rate'):
                    diff = int(current_hr) - digital_twin.predicted_heart_rate
                    if diff < 0:
                        self.swgt_interval_performance.setCurrentIndex(1)
                        self.lbl_interval_performance_up.setText(
                            str(diff)
                        )
                    else:
                        self.swgt_interval_performance.setCurrentIndex(2)
                        self.lbl_interval_performance_down.setText(
                            '+' + str(diff)
                        )

                # Interval average heart rate rendering.
                if hasattr(digital_twin, 'average_heart_rate'):
                    average_hr = digital_twin.average_heart_rate
                    if average_hr:
                        self.lbl_interval_average_heart_rate.setText(
                            str(int(average_hr))
                        )
                    else:
                        self.lbl_interval_proposed_heart_rate.setText('-')
            else:
                self.swgt_interval_performance.setCurrentIndex(0)

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
        minutes = int(time / 60) % 60
        hours = int(time / 60 / 60)

        time = (
            str(hours) +
            ':' +
            (str(minutes) if minutes > 9 else '0' + str(minutes)) +
            ':' +
            (str(seconds) if seconds > 9 else '0' + str(seconds))
        )

        return time


class HttpServerThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        """
        Initialization method for HttpServerThread class. The class is used for running a simple HTTP server that
        renders the Vue.js map component.
        """
        super().__init__()
        self.running = True

    def run(self):
        """
        Method that runs the HTTP server.
        """
        PORT = 8000
        Handler = CustomHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            self.signal.emit(f"Serving at http://localhost:{PORT}")
            while self.running:
                httpd.handle_request()

    def stop(self):
        """Method that stops the HTTP server."""
        self.running = False
