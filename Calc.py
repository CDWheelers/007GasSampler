import time
import math
from MCP3008 import *

adc = MCP3008() # Define Analog Digital Converter

class MQ():

    ######################### Hardware Related Macros #########################
    MQ_PIN                       = 0        # define which analog input channel you are going to use (MCP3008)
    RL_VALUE                     = 4.69     # define the total load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 1        # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived experimentally
 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 100      # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    GAS_NH3                      = 0        # Hardware Related Macro

    def __init__(self, Ro=19.3, analogPin=0):
        self.Ro = Ro
        self.MQ_PIN = analogPin
        self.adc = MCP3008()
        
        self.NH3Curve = [1.699,-0.678,-0.26]    # average slope is calculated from the datasheet
                                                # with this slope and approximated datapoint, a line is formed which is "approximately equivalent"
                                                # to the original curve. 
                                                # data format:{ x, y, slope}; point: (log50, -0.678)

        print("Calibrating...")
        self.Ro = self.MQCalibration(self.MQ_PIN)
        print("Calibration is done...\n")
        print("Ro=%f kohm" % self.Ro)
    
    
    def MQPercentage(self):
        val = {}
        read = self.MQRead(self.MQ_PIN)
        val["GAS_NH3"] = self.MQGetGasPercentage(read/self.Ro, self.GAS_NH3)
        return val
        
    ######################### MQResistanceCalculation #########################
    # Input:   val_adc - 12-bit value read from MCP3008 as a decimal representing total VRL
    # Output:  the calculated sensor resistance, Rs, for determining ammonia ppm
    # Remarks: The sensor and the (total) load resistance forms another voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQResistanceCalculation(self, val_adc):
        return float(self.RL_VALUE*(5-val_adc)/float(val_adc))
     
    ######################### MQCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          10, which differs slightly between different sensors.
    ############################################################################ 
    def MQCalibration(self, mq_pin):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):          # take multiple samples
            val += self.MQResistanceCalculation(self.ADCRead(mq_pin))
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBARAION_SAMPLE_TIMES                 # calculate the average value

        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 
                                                                
        return val;
      
    ######################### MQRead ###########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistance (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def MQRead(self, mq_pin):
        rs = 0.0

        for i in range(self.READ_SAMPLE_TIMES):
            rs += self.MQResistanceCalculation(self.ADCRead(mq_pin))
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs/self.READ_SAMPLE_TIMES

        return rs
     
    ######################### MQGetGasPercentage ###############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        gas_id == self.GAS_NH3
        return self.MQGetPercentage(rs_ro_ratio, self.NH3Curve)

    ######################### MQGetPercentage ##################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        return (math.pow(10,(((math.log10(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))
    
    ######################### ADCRead ##########################################
    # Input:   mq_pin - analog channel
    #          pcurve      - pointer to the curve of the target gas
    # Output:  VRL - Voltage across load resistance, RL_VALUE
    # Remarks: This process prepares raw adc data to be utilized by the rest of the program.
    #          first, raw ADC data is gathered directly from select adc channel. Then, Voltage
    #          division is undone to find VRL_adc, the bitwise interpretation of VRL voltage.
    #          VRL_adc mimics what the ADC's output would look like if it measured VRL directly,
    #          but recall that we do not measure VRL directly to protect the Raspberry Pi's GPIO pins.
    #          The ADC is powered with 3.3V, so a reading of 4095 corresponds to 3.3V, which is the
    #          maximum voltage that the Raspberry Pi can handle.
    #          VRL_adc is divided by 4095 and multiplied by 3.3 to normalize the reading
    ############################################################################ 
    def ADCRead(self, mq_pin):
        raw_adc = self.adc.read(mq_pin)
        
        VRL_adc = raw_adc * (4.69 / 1.57)                # redacts effect of load resistance voltage division
                                                             # raw_adc voltage measured is 1.57/4.69 of total VRL
                                                         
        VRL = VRL_adc * (3.3 / 4095)                     # converts from adc bitwise adc reading to true voltage
            
        return VRL
