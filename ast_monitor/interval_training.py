from threading import Thread
import time

from ast_monitor.digital_twin import DigitalTwin
from ast_monitor.write_log import WriteLog


class IntervalTraining:
    """
    Initialization method of the IntervalTraining class.\n
    Args:
        training: dict
            an interval training
        tick_time: int
            tick time in milliseconds
    """
    def __init__(self, training: dict, basic_data) -> None:
        """
        Initialization method of the IntervalTraining class.\n
        Args:
            training: dict
                an interval training
            tick_time: int
                tick time in milliseconds
        """
        self.file = training['file']
        self.name = training['interval'][0]['name']
        self.sport = training['interval'][0]['sport']
        self.info = training['interval'][0]['info']
        self.speed_duration = training['interval'][0]['speed_duration']
        self.recovery_duration = training['interval'][0]['recovery_duration']
        self.speed_heart_rate = training['interval'][0]['speed_heart_rate']
        self.recovery_heart_rate = (
            training['interval'][0]['recovery_heart_rate']
        )
        self.repetitions = training['interval'][0]['repetitions']
        self.type = training['interval'][0]['type']
        self.speed_notification = False
        self.recovery_notification = False
        self.phase_start = None
        self.abort_training = False
        self.basic_data = basic_data
        self.log = f'../logs/{self.file}.log'

    def __eq__(self, __o: object) -> bool:
        """
        Method for comparing two IntervalTraining objects.\n
        Args:
            __o: IntervalTraining
                an interval training to be compared to
        """
        return (
            self.name == __o.name and
            self.sport == __o.sport and
            self.info == __o.info and
            self.speed_duration == __o.speed_duration and
            self.recovery_duration == __o.recovery_duration and
            self.speed_heart_rate == __o.speed_heart_rate and
            self.recovery_heart_rate == __o.recovery_heart_rate and
            self.repetitions == __o.repetitions and
            self.type == __o.type
        )

    def start(self, write_log: bool = False) -> None:
        """
        Starting an interval training.\n
        Args:
            write_log: bool
                writing log if True
        """
        # Writing the header of the training.
        if write_log:
            WriteLog.write_interval_training_header(self.log)

        for i in range(self.repetitions):
            self.start_speed_phase(i, write_log=True)
            if self.abort_training:
                break
            self.start_recovery_phase(i, write_log=True)
            if self.abort_training:
                break
        self.abort_training = True

    def start_speed_phase(self, interval: int, write_log: bool) -> None:
        """
        Starting a speed phase of an interval.\n
        Args:
            interval: int
                index of the interval
            write_log: bool
                writing log if True
        """
        self.current_interval = interval, 'speed'
        self.speed_notification = True
        self.phase_start = time.time()
        self.time = time.time() - self.phase_start

        self.digital_twin = DigitalTwin(
            self.speed_heart_rate,
            self.speed_duration,
            tick_time=1000,
            basic_data=self.basic_data
        )
        self.digital_twin_thread = Thread(
            target=self.digital_twin.predict_heart_rate
        )
        self.digital_twin_thread.start()

        # Execution of a speed phase.
        while (
            not self.abort_training and
            self.time < 60 * self.speed_duration
        ):
            self.time = time.time() - self.phase_start
            WriteLog.write_interval_training_trackpoint(
                self.log,
                self.digital_twin
            )
            time.sleep(0.5)

    def start_recovery_phase(self, interval: int, write_log: bool) -> None:
        """
        Starting a recovery phase of an interval.\n
        Args:
            interval: int
                index of the interval
            write_log: bool
                writing log if True
        """
        self.current_interval = interval, 'recovery'
        self.recovery_notification = True
        self.phase_start = time.time()
        self.time = time.time() - self.phase_start

        self.digital_twin = DigitalTwin(
            self.recovery_heart_rate,
            self.recovery_duration,
            tick_time=1000,
            basic_data=self.basic_data
        )
        self.digital_twin_thread = Thread(
            target=self.digital_twin.predict_heart_rate
        )
        self.digital_twin_thread.start()

        # Execution of a recovery phase.
        while (
            not self.abort_training and
            self.time < 60 * self.recovery_duration
        ):
            self.time = time.time() - self.phase_start
            if write_log:
                WriteLog.write_interval_training_trackpoint(
                    self.log,
                    self.digital_twin
                )
            time.sleep(0.5)
