from sport_activities_features.hill_identification import HillIdentification


class SendData(object):
    """
    Class for sending data to the server and
    making the analysis of the training.
    """
    @staticmethod
    def send_data(data: list) -> None:
        """
        [WIP]
        Currently, the data is not sent to the API,
        instead, only some features from sport-activities-features
        are called.

        Sending data to the API.\n
        Args:
            data (list[SensorData]):
                training parameters
        """
        altitudes = []
        for trackpoint in data:
            altitudes.append(trackpoint.altitude)

        hill_identification = HillIdentification(altitudes, 30)
        hill_identification.identify_hills()
        hills = hill_identification.return_hills()
        print(hills)
