/*
 Copyright (c) 2018 Gaspare Caterino <shelladdicted@gmail.com>
   GitHub: ShellAddicted

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function handleResponse(data){
	console.log(data);
	var event = new Event('sensorRead');
	try{
		dt = JSON.parse(data);
		event.success = dt.success;
		event.isConnected = dt.isConnected;
		event.value = (dt.success === true) ? dt.value : -1;
	}
	catch(err){
		event.success = false;
		event.isConnected = false;
		event.value = -1;
	}
	window.dispatchEvent(event);
}

function wsInit(){
	ws = new WebSocket("ws://"+  document.location.host +"/api/ws");
	ws.onmessage = function(evt){
        handleResponse(evt.data);
	};
	ws.onclose = function(evt){
		handleResponse("{success: false, isConnected: false, value: -1}");
	}
    window.onbeforeunload = function(evt){
        ws.close();
    };
}

function refreshUsingWS(){
	if (ws.OPEN == true){
		ws.send(JSON.stringify({"cmd": "read"}));
	}
	else{
		wsInit(); //Reconnect
	}
}

wsInit();
refreshTask = window.setInterval(refreshUsingWS, 20);

/* USAGE:
window.addEventListener('sensorRead', function(e){
    if (e.value > 0.75){ // threshold: 75%
        // do something
    }
    else if (e.isConnected < 0){
        // Device failed the read or it is not connected
    }
    else if (e.deviceStatus === false){
        // device is not connected
    }
},false);
*/