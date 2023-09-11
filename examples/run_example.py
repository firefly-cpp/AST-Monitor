import os
import sys

from PyQt6 import QtWidgets

try:
    from ast_monitor.model import AST
except ModuleNotFoundError:
    sys.path.append('../')
    from ast_monitor.model import AST

# Paths to the files with heart rates and GPS data.
hr_data = '..' + os.sep + 'sensor_data' + os.sep + 'hr.txt'
gps_data = '..' + os.sep + 'sensor_data' + os.sep + 'gps.txt'
route_data = '..' + os.sep + 'development' + os.sep + 'routes' + os.sep + 'route.json'
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data, route_data)
    window.show()
    sys.exit(app.exec())
