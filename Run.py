from mq import *
import sys, time
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("NH3: %g ppm" % (perc["GAS_NH3"]))
        sys.stdout.write(" Voltage: %.3f V" % (mq.ADCRead(0)))
        sys.stdout.flush()
        time.sleep(0.1)

except Exception as e:
    logging.exception("An error occurred: %s", e)
