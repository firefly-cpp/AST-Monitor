from PyQt5 import QtWidgets
import sys
sys.path.append('../')

from ast_monitor.model import AST


# We need to provide two paths for storing sensor.
hr_data = '../sensor_data/hr.txt'
gps_data = '../sensor_data/gps.txt'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data)
    window.show()
    sys.exit(app.exec_())
