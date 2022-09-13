import time


class TrainingSession:
    """
    Class for tracking training sessions.
    """
    def __init__(self) -> None:
        self.start_time = time.time()
        self.time = 0.0
        self.distance = 0.0
        self.previous_elevation = None
        self.ascent = 0.0

    def calculate_time(self) -> None:
        """
        Method for calculating the current time of the session.
        """
        self.time = time.time() - self.start_time

    def add_distance(self, distance: float) -> None:
        """
        Adding to the total distance.\n
        Args:
            distance (float):
                distance in meters
        """
        self.distance += distance

    def add_ascent(self, current_elevation: float) -> None:
        """
        Adding to the total ascent.\n
        Args:
            current_elevation (float):
                current elevation in meters
        """
        if not self.previous_elevation:
            self.previous_elevation = current_elevation
            return

        diff = current_elevation - self.previous_elevation
        self.previous_elevation = current_elevation
        if diff > 0:
            self.ascent += diff
