Resources

ADC.py
- ADC python file adapted from: https://github.com/freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi
- Used as a development/calibration tool for confirming voltage and ADC readings


Calc.py, MCP3008.py, and Run.py
- Calc, MCP3008, and Run python files adapted from: https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ
- Tutorial: https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x
- MCP3008.py contains code that details what commands will be sent to the ADC
- Calc.py contains calculations to interpret raw ADC readings before being output in Run.py
- Note: The voltage divider acts as an analog logic level converter - the tutorial above utilizes a sensor with a digital output. A considerable amount of changes have been made.

app.log
- logs exceptions when there is a failure to run Run.py

Tutorial to get ALL of this to work:	

Setup Raspberry Pi:
	- Preliminary step: install following software to install Raspberry Pi OS on SD card: https://www.raspberrypi.com/software/
	- Before writing OS to SD card, press Ctrl+Shift+X while the Imager is open, OS Customization tab should open
	- Under "General" check "Set hostname" and set to "raspberrypi.local"
	- Under "General" check "Set username and password" and pick secure username and password
	- Under "General" check "Configure Wireless LAN" and SSID and password should be consistent with local wireless network that you have access to
	- Under "Services" press "Enable SSH" and "Use Password Authentication"
	- Under "Options" check "Enable Telemetry"
	- Finally, Install Raspberry Pi OS 64-bit on SD card and insert SD card in Raspberry Pi once complete

Setup VNC (Optional, recommended for testing & adding new features):
	- With Raspberry Pi powered on, connect to Raspberry Pi wirelessly through your desktop. Open Command Prompt and type "ssh raspberrypi.local"
	- Enter the password that you set up before
	- Now that connection with Pi is established, type "sudo raspi-config" the Raspberry Pi Software Configuration Tool should appear
	- Navigate down to "Interface" and press "Enter" then Navigate to "VNC" and Press "Yes" to enable VNC Server
	- Press "Ok" to return back to main page, then "Finish" to return back to cmd
	- Type "ifconfig" and seek the row denoted by "wlan0" and seek the "inet" LAN IP address within the first row underneath "wlan0" (ex: 192.168.1.241)
	- This number will be used to access the Raspberry Pi through the VNC Viewer using the password and username decided previously

Setup SPI:
	- With Raspberry Pi powered on, connect to Raspberry Pi wirelessly through your desktop (VNC Viewer or Windows Comand Prompt)
		- VNC: Connect to Raspberry Pi through VNC Viewer using LAN IP discovered previously and password and username determined before. Open Terminal
		- CMD: With Raspberry Pi powered on, connect to Raspberry Pi wirelessly through your desktop. Open Command Prompt and type "ssh raspberrypi.local" then enter password
	- Now that connection with Pi is established, type "sudo raspi-config" the Raspberry Pi Software Configuration Tool should appear
	- Navigate down to "Interface" and press "Enter" then Navigate to "SPI" and Press "Yes" to enable SPI Interface
	
Setup Python 3:
	- Connect to Raspberry Pi
	- Type "cd /usr/bin" enter directory
	- Type "sudo rm python" delete old python link
	- Type "sudo ln -s python3 python" create new python links to python 3
	- Type "python" execute python to check whether link succeeds. result should be current python version (python 3.X.X) displayed

Install SpiDev:
	- Connect to Raspberry Pi through VNC Viewer or Windows Command Prompt
	- Type "sudo apt-get install python3-spidev" to install SpiDev package

Update Raspberry Pi:
	- Connect to Raspberry Pi through VNC Viewer or Windows Command Prompt
	- Type "sudo apt update && sudo apt full-upgrade" to fully upgrade Raspberry Pi

Install This Code:
	- Connect to Raspberry Pi through VNC Viewer or Windows Command Prompt
	- Type "git clone https://github.com/CDWheelers/007GasSampler" to install this package
 	- This package will be installed to path: /home/user/007GasSampler

Update This Code:
	- Connect to Raspberry Pi through VNC Viewer or Windows Command Prompt
	- Type "cd 007GasSampler" to navigate to path of cloned repository
 	- Type "git pull" and repository will be updated to reflect what is uploaded on https://github.com/CDWheelers/007GasSampler

Run This Code:
  	- Type "cd 007GasSampler" then "sudo python Run.py" to run the calibration and sensing code, outputs ppm of ammonia nearby, Ro of sensor, and load voltage


   
