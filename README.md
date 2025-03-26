Resources:

ADC.py:
- ADC python file adapted from: https://github.com/freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi
- Used as a development/calibration tool for confirming voltage and ADC readings

Calc.py, MCP3008.py, and Run.py:
- Calc, MCP3008, and Run python files adapted from: https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ
- MCP3008.py contains code that details what commands will be sent to the ADC
- Calc.py contains calculations to interpret raw ADC readings before being output in Run.py
- Note: The voltage divider acts as an analog logic level converter - the tutorial above utilizes a sensor with a digital output. A considerable amount of changes have been made



Tutorial to get ALL of this to work:	

Setup Raspberry Pi:
	- Preliminary step: install following software to image Raspberry Pi OS on SD card: https://www.raspberrypi.com/software/
	- Before writing OS to SD card, press Ctrl+Shift+X while the Imager is open, OS Customization tab should open
	- Under "General" check "Set hostname" and set to "raspberrypi.local"
	- Under "General" check "Set username and password" and pick secure username and password
	- Under "General" check "Configure Wireless LAN" and SSID and password should be consistent with local wireless network that you have access to
	- Under "Services" press "Enable SSH" and "Use Password Authentication"
	- Under "Options" check "Enable Telemetry"
	- Finally, Install Raspberry Pi OS 64-bit on SD card and insert SD card in Raspberry Pi once complete
	- Turn Raspberry Pi on, then connect to Raspberry Pi wirelessly through your desktop command prompt
 
		- In the command prompt, enter the command "ssh raspberrypi.local"
		- In the event authenticity of the host cannot be established, type "yes" when prompted to continue connecting and/or follow the instructions to add correct host key in C:\\Users\\User/.ssh/known_hosts, then try connecting through ssh command again
		- Enter the password you chose previously when prompted

		If connection cannot be made this way, follow these steps instead:

		- In the command prompt, enter the command "ping raspberrypi.local"
		- The result should look something like this:

		""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
				Pinging raspberrypi.local [2600:1700:60c:8210:7370:e25c:ebeb:1f4e] with 32 bytes of data:
				Reply from 2600:1700:60c:8210:7370:e25c:ebeb:1f4e: time=3ms
				Reply from 2600:1700:60c:8210:7370:e25c:ebeb:1f4e: time=7ms
				Reply from 2600:1700:60c:8210:7370:e25c:ebeb:1f4e: time=6ms
				Reply from 2600:1700:60c:8210:7370:e25c:ebeb:1f4e: time=6ms

				Ping statistics for 2600:1700:60c:8210:7370:e25c:ebeb:1f4e:
    					Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
				Approximate round trip times in milli-seconds:
    					Minimum = 3ms, Maximum = 7ms, Average = 5ms
		""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

		- Copy the inet6 address listed above (in this case, 2600:1700:60c:8210:7370:e25c:ebeb:1f4e). Enter the command "ssh (the address)" into the command prompt (i.e. "ssh 2600:1700:60c:8210:7370:e25c:ebeb:1f4e" for me)
		- In the event authenticity of the host cannot be established, type "yes" when prompted to continue connecting and/or follow the instructions to add correct host key in C:\\Users\\User/.ssh/known_hosts, then try connecting through ssh command again
		- Enter the password you chose previously when prompted.

	Once connection is made:
	- By now, your desktop command prompt should be that of the Raspberry Pi's. If you see "user@raspberrypi:~ $" where "C:\Users\User>" should be, you are now viewing the terminal of your Raspberry Pi, remotely
	- Enter command "sudo raspi-config" the Raspberry Pi Software Configuration Tool should appear
		- Enable SPI: Navigate down to "Interface" and press "Enter" then navigate to "SPI" and press "Yes" to enable SPI interface. Note: SSH is already enabled from the Raspberry Pi Imager, don't disable it here
		- Enable VNC: Again, in "Interface," navigate to "VNC" and press "Yes" to enable VNC control of the Raspberry Pi (OPTIONAL, BUT HIGHLY RECCOMENDED - See Setup VNC below for extended tutorial)
	- Navigate to to the "Finish" button at the bottom of the Software Configuration Tool and press enter to navigate back to the Raspberry Pi terminal still remotely hosted by your command prompt
	- Enter command "sudo apt update && sudo apt full-upgrade" to fully upgrade Raspberry Pi, and follow onscreen instructions
	- Enter command "git clone https://github.com/CDWheelers/007GasSampler" to install this package
 		- This package will be installed to path: /home/user/007GasSampler
		- Enter "cd 007GasSampler" to navigate to path of cloned repository and type "git pull" to update repository as needed periodically


To Run Code:
	- Through ssh connection via command prompt, enter "cd 007GasSampler" then "sudo python ___.py" to run your desired script	
	- Through VNC, simply navigate to the script you wish to run, open it, and press the Run arrow at the top
	- Drone should be executing the Run.py script ONLY. Run.py calibrates the sensor first, then reads sensor data, connects to the GCS via server function, and transmits data.

Setup VNC (Optional, recommended for testing & adding new features):
	- With Raspberry Pi powered on, connect to Raspberry Pi wirelessly through your desktop. Open Command Prompt and type "ssh raspberrypi.local"
	- Enter the password that you set up before
	- Now that connection with Pi is established, type "sudo raspi-config" the Raspberry Pi Software Configuration Tool should appear
	- Navigate down to "Interface" and press "Enter" then Navigate to "VNC" and Press "Yes" to enable VNC Server
	- Press "Ok" to return back to main page, then "Finish" to return back to cmd
	- Type "ifconfig" and seek the row denoted by "wlan0" and seek the "inet" LAN IP address within the first row underneath "wlan0" (in my case, 192.168.1.241)
	- I'm using RealVNC Viewer, I selected "Create New Connection" using the Raspberry Pi's LAN IP address (in my case, 192.168.1.241) as the VNC Server IP
	- Access the Raspberry Pi through the VNC Viewer using the password and username decided previously
	- You can now view and navigate the Raspberry Pi's Virtual Desktop, as well as edit/verify any code with ease.



If you're having issues, make sure SpiDev and Python 3 are installed (they should be, by default):

Setup Python 3:
	- Connect to Raspberry Pi
	- Type "cd /usr/bin" enter directory
	- Type "sudo rm python" delete old python link
	- Type "sudo ln -s python3 python" create new python links to python 3
	- Type "python" execute python to check whether link succeeds. result should be current python version (python 3.X.X) displayed

Install SpiDev:
	- Connect to Raspberry Pi through VNC Viewer or Windows Command Prompt
	- Type "sudo apt-get install python3-spidev" to install SpiDev package
