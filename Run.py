from Calc import *
from gps_from_pixhawk import get_gps_data
import sys, time
import logging
from datetime import datetime

# Start server.py script in a separate process
server_process = subprocess.Popen(["python", "server.py"])

logging.basicConfig(filename='app.log', level=logging.ERROR)

filename = "data.txt"
delay = float(2.0000)
decimal_places = int(4)

try:
    print("Press CTRL+C to abort.")
    
    with open(filename, 'w') as file: #'w' overwrites file of same filename, 'a' appends
        print(f"Writing random numbers to '{filename}'... Press Ctrl+C to stop.\n")

    mq = MQ()
    
    while True:

        lat, lon = get_gps_data()

        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("NH3: %g ppm" % (perc["GAS_NH3"]))
        sys.stdout.write(" Voltage: %.4f V" % (mq.ADCRead(0)))
        sys.stdout.flush()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4] # Get current timestamp
        file.write(f"{timestamp}, {lat:.6f}, {lon:.6f}, {perc['GAS_NH3']:.4f}\n")
        file.flush()  # Ensure immediate writing to the file from program buffer
        print(f"Written {perc['GAS_NH3']:.4f}ppm at {timestamp}")
        time.sleep(0.1)

except Exception as e:
    logging.exception("An error occurred: %s", e)
