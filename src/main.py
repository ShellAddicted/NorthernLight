# Copyright (c) 2018 Gaspare Caterino <shelladdicted@gmail.com>
#   GitHub: ShellAddicted
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#---------------------------------------------------------------------

# PySerial Module is under BSD-3-Clause license
# Copyright (c) 2001-2016 Chris Liechti <cliechti@gmx.net>
# All Rights Reserved.

#---------------------------------------------------------------------

# Tornado module is under Apache 2.0 License
# Copyright 2015 The Tornado Authors

#---------------------------------------------------------------------

import sys
import logging

from MainWindow import MainWindow

try:
    from PySide2 import QtWidgets, QtGui, QtCore
except ImportError:
	raise ImportError("PySide2 not found, install it.")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(".", "northernlight")),
            logging.StreamHandler()
        ]
    )
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()