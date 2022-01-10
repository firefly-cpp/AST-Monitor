from PyQt5 import QtCore, QtGui, uic, QtWidgets
from ast_monitor.ast import AST
import sys

# we need to provide two paths for storing sensor data

hr_data = "sensor_data/hr.txt"
gps_data = "sensor_data/gps.txt"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data)

    window.show()
    sys.exit(app.exec_())
