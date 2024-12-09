import time
from MCP3008 import MCP3008

adc = MCP3008() 

# This code is designed to test the MCP3008 Analog-Digital Converter
# With channel 0 measuring divided, partial voltage from the center of the voltage divider
# Voltage divider reversal already occurs in MCP3008.py
# Script will output measured VRL according to the ADC

# MCP3008 is powered with 3.3V to keep RPi GPIO pins safe
# value = adc.read(0) ranges from 0 to 4095 as a digital measure of voltage
# Where value = 4095 represents 3.3V reading and value = 0 reprepesents 0V reading in channel 0

def loop():                         
    while True:                                   
        value = adc.read(0)                       # read the ADC value of channel 0
        voltage = value / 4095 * 3.3              # calculate the voltage value of from adc integer binary number
                                                      
        print ('ADC Value : %d, Voltage : %.2f,' %(value,voltage))
        time.sleep(0.1)

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        print("Ending program")
        
