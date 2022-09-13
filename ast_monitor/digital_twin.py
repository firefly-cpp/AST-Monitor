import time


class DigitalTwin:
    """
    Class that represents a digital twin that
    uses a mathematical prediction model to
    analyze an exercise in the real time.\n
    Args:
        predicted_heart_rate (int):
            a predicted heart rate of an interval
            (speed or rest segment) in beats per minute
        duration (int):
            duration of an interval in minutes
    """
    def __init__(
        self,
        proposed_heart_rate: int,
        duration: int,
        tick_time: float,
        basic_data
    ) -> None:
        """
        Initialization method of the DigitalTwin class.\n
        Args:
            predicted_heart_rate (int):
                a predicted heart rate of an interval
                (speed or rest segment) in beats per minute
            duration (int):
                duration of an interval in minutes
            tick_time (float):
                a tick time in seconds
        """
        self.proposed_heart_rate = proposed_heart_rate
        self.predicted_duration = 60 * duration
        self.current_heart_rate = 0
        self.start_time = time.time()
        self.expected_trackpoints = (60 * 1000 * duration) // tick_time
        self.basic_data = basic_data

    def read_control_data(self) -> tuple:
        """
        Reading the current heart rate and the interval duration.\n
        Returns:
            tuple[int, float]: current heart rate, current duration
        """
        # Reading the current heart rate.
        hr = self.basic_data.current_heart_rate
        if hr:
            hr = int(hr)

        # Calculating the current phase time.
        phase_time = time.time() - self.start_time

        return hr, phase_time

    def calculate_prediction(
        self,
        trimp_delta: float,
        average_heart_rate: float,
        proposed_heart_rate: int,
        time_delta: float,
        expected_trackpoints: int
    ) -> float:
        """
        Calculating the predicted heart rate.\n
        Args:
            trimp_delta (float):
                the calculated TRIMP difference
            average_heart_rate (float):
                the average heart rate of the interval in beats per minute
            proposed_heart_rate (int):
                the proposed heart rate of the interval in beats per minute
            time_delta (float):
                the time difference in seconds
            expected_trackpoints (int):
                the number of expected trackpoints
        Returns:
            float: the proposed heart rate
        """
        if trimp_delta < 0:
            self.minus += trimp_delta
        else:
            self.plus += trimp_delta

        if average_heart_rate < proposed_heart_rate:
            return proposed_heart_rate
        else:
            return (
                proposed_heart_rate +
                (self.minus - self.plus) / (expected_trackpoints * time_delta)
            )

    def predict_heart_rate(self) -> None:
        """
        Digital twin algorithm that monitors the athlete
        performance in the real time and calculates the
        predicted heart rate.
        """
        n = 1
        current_time = 0
        current_heart_rate = 0
        previous_heart_rate, previous_time = self.read_control_data()
        self.average_heart_rate = previous_heart_rate
        time_delta = 0
        self.minus, self.plus = 0, 0

        while current_time <= self.predicted_duration - 1:
            # Reading the current heart rate and the duration.
            current_heart_rate, current_time = self.read_control_data()

            time_delta = current_time - previous_time
            if time_delta == 0:
                continue

            if self.predicted_duration - 1 <= current_time:
                break

            if current_heart_rate and previous_heart_rate:
                # Calculating the average heart rate and the time difference.
                if self.average_heart_rate:
                    self.average_heart_rate = (
                        self.average_heart_rate +
                        (1 / n) * (
                            current_heart_rate - self.average_heart_rate
                        )
                    )
                else:
                    self.average_heart_rate = current_heart_rate

                # Calculating the TRIMP difference.
                trimp_delta = (
                    ((current_heart_rate - previous_heart_rate) / 2) *
                    time_delta -
                    self.proposed_heart_rate * time_delta
                )

                # Predicted heart rate calculation.
                self.predicted_heart_rate = self.calculate_prediction(
                    trimp_delta,
                    self.average_heart_rate,
                    self.proposed_heart_rate,
                    self.predicted_duration - current_time,
                    self.expected_trackpoints
                )
                if self.predicted_heart_rate:
                    self.predicted_heart_rate = round(
                        self.predicted_heart_rate
                    )

                n += 1

            previous_time = current_time
            previous_heart_rate = current_heart_rate
            time.sleep(0.5)
