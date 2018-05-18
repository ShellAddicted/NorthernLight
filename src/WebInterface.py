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
import asyncio
import json

try:
	import tornado.ioloop
	import tornado.web
	import tornado.websocket
except ImportError:
	raise ImportError("Tornado not found, install it. ex: pip install Tornado")

try:
	from PySide2 import QtWidgets, QtGui, QtCore
except ImportError:
	raise ImportError("PySide2 not found, install it.")

class wsHandler(tornado.websocket.WebSocketHandler):
	def on_message(self, msg):
		# Sample Websocket message structure JSON: {"cmd":"read"}
		try:
			cmd = json.loads(msg)
			if cmd["cmd"] == "read":
				res = {"success": True, "value": self.application.lastReadValue, "isConnected": self.application.deviceStatus}
			else:
				res = {"success": False, "reason": "unknown command"}
		except Exception:
			res = {"success": False, "reason": "Internal Error"}

		self.write_message(json.dumps(res))

class apiHandler(tornado.web.RequestHandler):
	def get(self,*args, **kwargs):
		self.clear()
		self.set_status(200)
		self.set_header("Content-Type", "application/json")
		try:
			if self.request.path == "/api/read":
				res = {"success": True, "value": self.application.lastReadValue, "isConnected": self.application.deviceStatus}
			else:
				res = {"success": False, "reason": "unknown command"}
		except Exception:
			res = {"success": False, "reason": "Internal Error"}
		self.write(json.dumps(res))

class WebInterface(QtCore.QThread):

	def __init__(self, address="0.0.0.0", port=8383):
		super(WebInterface,self).__init__()
		self._address = address
		self._port = port

	def run(self):
		self._aloop = asyncio.new_event_loop() # Create an async loop for the current Thread
		asyncio.set_event_loop(self._aloop)
		self._server = tornado.web.Application([
				(r"/api/ws", wsHandler),
				(r"/api/(.*)", apiHandler),
				(r"/(.*)", tornado.web.StaticFileHandler, {"path": "./documentRoot","default_filename": "index.html"})
		])
		self._server.lastReadValue = -1
		self._server.deviceStatus = False		
		self._server.listen(self._port)
		tornado.ioloop.IOLoop.current().start()

	def updateValue(self, value):
		self._server.lastReadValue = value

	def updateDeviceStatus(self, value):
		self._server.deviceStatus = value

	def stopTornado(self):
		asyncio.set_event_loop(self._aloop)
		lq = tornado.ioloop.IOLoop.current()
		lq.add_callback(lq.stop)