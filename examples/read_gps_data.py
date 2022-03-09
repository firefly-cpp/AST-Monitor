from ast_monitor.gps_sensor import GpsSensor


# Where to store data.
path = 'sensor_data/gps.txt'

gps = GpsSensor(gps_path=path)
gps.get_gps_data()
