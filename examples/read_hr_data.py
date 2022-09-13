try:
    from ast_monitor.hr_sensor import HrSensor
except Exception:
    import sys
    sys.path.append('../')
    from ast_monitor.hr_sensor import HrSensor


# Path to the file where heart rate data will be saved to.
path = '../sensor_data/hr.txt'

hr = HrSensor(hr_path=path)
hr.get_hr_data()
