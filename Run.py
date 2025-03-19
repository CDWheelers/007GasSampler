from Calc import *
import sys, time
import logging
from datetime import datetime

logging.basicConfig(filename='app.log', level=logging.ERROR)

filename = "data.txt" # For testing purposes
min_val = float(0.0000)
max_val = float(100.0000)
delay = float(2.0000)
decimal_places = int(4)

try:
    print("Press CTRL+C to abort.")
    
    with open(filename, 'w') as file: #'w' overwrites file of same filename, 'a' appends
        print(f"Writing random numbers to '{filename}'... Press Ctrl+C to stop.\n")

    mq = MQ();
    
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("NH3: %g ppm" % (perc["GAS_NH3"]))
        sys.stdout.write(" Voltage: %.4f V" % (mq.ADCRead(0)))
        sys.stdout.flush()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4] # Get current timestamp
        file.write(f"{timestamp} - {mq.ADCRead(0)} ppm\n")
        file.flush()  # Ensure immediate writing to the file from program buffer
        print(f"Written {mq.ADCRead(0)}ppm at {timestamp}")
        time.sleep(0.1)

except Exception as e:
    logging.exception("An error occurred: %s", e)
