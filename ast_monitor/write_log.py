from datetime import datetime
import time


class WriteLog:
    """
    Class for writing log.
    """
    @staticmethod
    def write_interval_training_header(file: str):
        """
        Method for writing interval training header.\n
        Args:
            file: str
                path to the log file
        """
        path = f'../logs/{file}'
        time_s = datetime.utcnow().isoformat()
        with open(path, 'a') as log:
            log.write(f'\n[{time_s}] {file}\n')
            log.write('Log parameters: HR_prop, HR_avg, HR_pred, t\n')

    @staticmethod
    def write_interval_training_trackpoint(file: str, digital_twin):
        """
        Method for writing interval training trackpoint.\n
        Args:
            file: str
                path to the log file
            digital_twin: DigitalTwin
                the Digital Twin
        """
        path = f'../logs/{file}'
        time_s = datetime.utcnow().isoformat()
        predicted_hr = '-'
        proposed_hr = str(int(digital_twin.proposed_heart_rate))
        average_hr = '-'
        phase_time = str(round(time.time() - digital_twin.start_time, 3))

        if hasattr(digital_twin, 'predicted_heart_rate'):
            predicted_hr = str(int(digital_twin.predicted_heart_rate))
        if digital_twin.average_heart_rate:
            average_hr = str(int(digital_twin.average_heart_rate))

        with open(path, 'a') as log:
            log.write(
                f'[{time_s}]' + ' ' +
                proposed_hr + ' ' +
                average_hr + ' ' +
                predicted_hr + ' ' +
                phase_time + '\n'
            )
