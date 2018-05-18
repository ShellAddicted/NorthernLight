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
	import serial.tools.list_ports
except ImportError:
	raise ImportError("pyserial not found, install it. ex: pip install pyserial")
	
try:
	from PySide2 import QtWidgets, QtGui, QtCore
except ImportError:
	raise ImportError("PySide2 not found, install it.")

from SerialHandler import SerialHandler
from WebInterface import WebInterface

def _(message):return message # TODO: internationalize

class MainWindow(QtWidgets.QWidget):

	def __init__(self, rescanDelayMS = 250, port = 8989, handlers = [SerialHandler]):
		super(MainWindow, self).__init__()
		self._rescanDelayMS = rescanDelayMS
		self._port = port
		self._handlers = handlers

		self.selectDeviceLab = QtWidgets.QLabel(_("Select the device:"))
		self.selectDevice = QtWidgets.QComboBox()
		self.selectDevice.activated.connect(self.deviceChanged)

		self.deviceSelectionLay = QtWidgets.QVBoxLayout()
		self.deviceSelectionLay.addWidget(self.selectDeviceLab)
		self.deviceSelectionLay.addWidget(self.selectDevice)
		self.deviceSelectionLay.setAlignment(QtCore.Qt.AlignTop)

		self.WebUIUrlLab = QtWidgets.QLabel(_("WebUI:"))
		self.WebUIUrl = QtWidgets.QLabel()
		self.WebUIUrl.setText('<a href="http://localhost:{0}">WebUI @ http://localhost:{0}</a>'.format(self._port))
		self.WebUIUrl.setStyleSheet("QLabel {font-size:32pt;}")
		self.WebUIUrl.setOpenExternalLinks(True)
		self.WebUIUrl.setTextFormat(QtCore.Qt.RichText)
		self.WebUIUrl.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
		
		self.WebUIUrlLay = QtWidgets.QVBoxLayout()
		self.WebUIUrlLay.addWidget(self.WebUIUrlLab)
		self.WebUIUrlLay.addWidget(self.WebUIUrl)
		self.WebUIUrlLay.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)

		self.progressLab = QtWidgets.QLabel(_("Current Value:"))
		self.progress = QtWidgets.QProgressBar()
		self.progress.setValue(0)

		self.progressLay = QtWidgets.QVBoxLayout()
		self.progressLay.addWidget(self.progressLab)
		self.progressLay.addWidget(self.progress)
		self.progressLay.setAlignment(QtCore.Qt.AlignBottom)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.addLayout(self.deviceSelectionLay)
		self.mainLayout.addLayout(self.WebUIUrlLay)
		self.mainLayout.addLayout(self.progressLay)

		self.setLayout(self.mainLayout)

		self.setWindowTitle(_("NorthernLight"))
		self.resize(300,300)

		self.wi = WebInterface(port = self._port)
		self.wi.start()
		
		self.activeHandler = None

		self._devices = []
		self.rescanDevices()
		self._rescanTimer = QtCore.QTimer(self)
		self._rescanTimer.timeout.connect(self.rescanDevices)
		self._rescanTimer.start(self._rescanDelayMS)

	def updateValue(self, value):
		self.wi.updateValue(value)
		self.progress.setValue(0 if value < 0 else value*100)

	def updateDeviceStatus(self, value):
		self.wi.updateDeviceStatus(value)
		if value:
			self._rescanTimer.stop()
			for ix in range(self.selectDevice.count()):
				deviceIndex = self.selectDevice.itemData(ix)
				if deviceIndex is not None:
					currentDevice = self._devices[deviceIndex].getConnectedDevice()
					if currentDevice is not None and currentDevice == self.activeHandler.getConnectedDevice():
						self.selectDevice.setCurrentIndex(ix)
		else:
			self.updateValue(-1)
			self._rescanTimer.start(self._rescanDelayMS)

	def rescanDevices(self):
		self._devices = []
		self.selectDevice.clear()
		
		for handler in self._handlers:
			self._devices += handler.listDevices()

		if len(self._devices) == 0:
			self.selectDevice.addItem(_("Device Not found."), None)
			self.selectDevice.setDisabled(True)
		else:
			self.selectDevice.addItem(_("Select a device."), None)
			for index, device in zip(range(len(self._devices)),self._devices):
				self.selectDevice.addItem(str(device.deviceName), index)
			self.selectDevice.setDisabled(False)

	def closeEvent(self, event):
		if self.activeHandler.isRunning:
			self.activeHandler.stop()
			self.activeHandler.wait(5)
			
		if self.wi.isRunning:
			self.wi.stopTornado()
			self.wi.wait(5)

	def deviceChanged(self, event = None):
		if self.activeHandler is not None:
			self.activeHandler.stop()
			self.activeHandler.wait(5)

		deviceIndex = self.selectDevice.currentData()
		if deviceIndex is not None:
			self.activeHandler = self._devices[deviceIndex]
			self.activeHandler.value.connect(self.updateValue)
			self.activeHandler.connectionState.connect(self.updateDeviceStatus)
			self.activeHandler.start()
		