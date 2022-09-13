try:
    from ast_monitor.gps_sensor import GpsSensor
except Exception:
    import sys
    sys.path.append('../')
    from ast_monitor.gps_sensor import GpsSensor


# Path to the file where GPS data will be saved to.
path = '../sensor_data/gps.txt'

gps = GpsSensor(gps_path=path)
gps.get_gps_data()
