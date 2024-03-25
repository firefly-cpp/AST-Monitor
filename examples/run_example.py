import os
import sys

from PyQt6 import QtWidgets

try:
    from ast_monitor.model import AST
except ModuleNotFoundError:
    sys.path.append('../')
    from ast_monitor.model import AST

# Paths to the files with heart rates and GPS data.
hr_data = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), '..', 'sensor_data', 'hr.txt')
gps_data = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', 'sensor_data', 'gps.txt')
route_data = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), '..', 'development', 'routes', 'route.json')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data, route_data)
    window.show()
    sys.exit(app.exec())
