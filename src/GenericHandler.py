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

import logging

try:
    from PySide2 import QtCore
except ImportError:
	raise ImportError("PySide2 not found, install it.")

class GenericHandler(QtCore.QThread):
	# GenericHandler must support initialization with 'None' device
	value = QtCore.Signal(float) # Device handler must notify value updates over value (qt)signal
	connectionState = QtCore.Signal(bool) # Device handler must notify state of connection changes over connectionState (qt)signal

	def getConnectedDeviceName(self):
		# Return device name to show in UI as string
		raise NotImplementedError()

	def getConnectedDevice(self):
		#return a *unique* identifier of the connected device (like /dev/ttyUSB0)
		raise NotImplementedError()

	def isConnected(self):
		# must return a bool with the current state of the connection with device
		# True -> Connected
		# False -> Disconnected
		raise NotImplementedError()
	
	def getValue(self):
		# must return the last value read from device, as float (value < 0.0 means read fail) [0.3 means 30%]
		raise NotImplementedError()

	@staticmethod
	def listDevices():
		# Must return a list() of instances of your handler (one instance for each device)
		# example of the structure: [handler(device1),handler(device2), handler(deviceN...)]
		# where handler is a class derivated from GenericHandler 
		raise NotImplementedError()

	def stop(self):
		# Disconnects from the device and stop the QThread (timeout = 5secs)
		# handler should emit connectionState -> False on quit.
		raise NotImplementedError()
