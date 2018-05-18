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

# Import PySerial
try:
	import serial
except ImportError:
	raise ImportError("pyserial not found, install it. ex: pip install pyserial")

try:
    from PySide2 import QtCore
except ImportError:
	raise ImportError("PySide2 not found, install it.")

from GenericHandler import GenericHandler

class SerialHandler(GenericHandler):

	def __init__(self, device, deviceName = "", baudrate = 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=1, timeout=1):
		"""
		Serial defaults -> 115200 8N1
		"""
		super(SerialHandler,self).__init__()
		self._device = device
		self._baudrate = baudrate
		self._bytesize = bytesize
		self._parity = parity
		self._stopbits = stopbits
		self._timeout = timeout

		self._log = logging.getLogger("SerialHandler")
		self._serialConnection = None

		self._flag = True
		self._lastValue = None
		self.deviceName = deviceName

	def __del__(self):
		self.stop()

	def getConnectedDevice(self):
		return self._device

	@staticmethod
	def listDevices():
		return [SerialHandler(port.device, str(port)) for port in list(serial.tools.list_ports.comports())]

	def isConnected(self):
		try:
			return self._serialConnection.is_open
		except Exception:
			return False

	def getValue(self):
		return self._lastValue

	def stop(self):
		self._flag = False

	def run(self):
		while self._flag:
			try:
				self.connectionState.emit(False)							# Not (yet) connected with the device

				if self._device in (None, ""):
					self._log.error("Can't connect to {0} (None) device".format(self._device))
					return 1

				self._log.info("Connecting to {0} @ {1} baud {2}-{3}-{4}".format(self._device,self._baudrate,self._bytesize,self._parity,self._stopbits))
				self._serialConnection = serial.Serial(self._device, self._baudrate, bytesize=self._bytesize, parity=self._parity, stopbits=self._stopbits, timeout=self._timeout)
				self._serialConnection.read_all()							# Clear OS Buffer
				self.connectionState.emit(True)								# Connection established
				self._log.info("Connected.")

				while self._flag:
					self._log.debug("Reading 2 bytes...")
					try:
						data = self._serialConnection.read(2)               # Read 2 Bytes
						if (len(data) == 2 and data[0] == 0xFB):            # Got 2 Bytes and ControlCode is 0xFB (OK)
							self._lastValue = float(data[1])/100
						else:                                               # Got malformed data
							self._log.error("Bad Format")
							self._serialConnection.read_all()               #Clear OS Buffer
							self._lastValue = float(-1)
						self.value.emit(self._lastValue)                    #Notify Failed Read (value = -1)

					except serial.serialutil.SerialException as exc:		# Serial Exception (Fatal) (maybe Devices has been disconnected?)
						raise exc											# Let it handle by the upper Exception handler

					except Exception:										# Log Exception and continue (Doesn't reconnect)
						self._log.error("exc", exc_info=True)
						continue

			except (serial.serialutil.SerialException, FileNotFoundError):  # Serial Exception (fatal) (maybe Devices has been disconnected?)
				self._log.fatal("exc", exc_info=True)
				self.value.emit(-1)
				break                                                       # Close Everything && Terminate

			except Exception:
				self._log.error("exc", exc_info=True)                       # Log Error Message && Continue (reconnect if necessary)
				self.value.emit(-1)

			finally:
				try:self._serialConnection.close()
				except Exception:pass
				self._log.info("Disconnected.")
				self.connectionState.emit(False)							# Disconnected
				self.value.emit(-1)