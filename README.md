# NorthernLight
An interface between a (local) Web UI and host machine.

# Description
This application provides a Web server & a WebSockets server that can feed a WebUI with information from a local device
or even the local machine.

for DEMO purposes this application is predisposed to read a single value, but you can easily fork this and customize it for your needs.

## DEMO
Read ADC value from an Arduino over Serial Interface as a percentage (%)
- flash [src/arduinoCode.cpp](https://github.com/ShellAddicted/NorthernLight/blob/master/src/arduinoCode.cpp) into your arduino.
- launch [main.py](https://github.com/ShellAddicted/NorthernLight/blob/master/src/main.py) from root the directory of repository  
Correct: `python3 src/main.py`  
Wrong: ~~cd src/ && python3 [main.py](https://github.com/ShellAddicted/NorthernLight/blob/master/src/main.py)~~
- select the correct device
- Open the default URL

# Requirements
- Tornado==5.0.2
- PySide2==5.11
- pyserial==3.4

# Do you want to use this for your own software? DO IT!
- Create a DeviceHandler(derivate from GenericHandler) for your own device (or data source)
- Register your handler in MainWindow(handlers=[...])
- Place your WebUI files (html,css,images,etc...) in [documentRoot/](https://github.com/ShellAddicted/NorthernLight/blob/master/documentRoot/northernlight.js)
- Launch the app & select the correct device.
- Enjoy your WebUI!

for more details see [GenericHandler.py](https://github.com/ShellAddicted/NorthernLight/blob/master/src/GenericHandler.py) and [northernlight.js](https://github.com/ShellAddicted/NorthernLight/blob/master/documentRoot/northernlight.js)  
also check [SerialHandler.py](https://github.com/ShellAddicted/NorthernLight/blob/master/src/SerialHandler.py) as a reference implementation.
 
but remember to respect the [License](https://github.com/ShellAddicted/NorthernLight/blob/master/license)!  

# FAQ
## Why did you named it 'NorthernLight'?
Because I have not (yet) decided an official name so I will keep temporary this codename that I used in development.

