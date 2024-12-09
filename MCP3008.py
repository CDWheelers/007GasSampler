from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.mode = 0
        self.spi.max_speed_hz = 1000000 # 1MHz          # Set SPI speed

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz          
    
    ######################### MCP3008.read #####################################
    # Input:   channel - channel to be read from
    # Output:  data - decimal result of binary MCP3008 reading, represents voltage across entire load resistance RL = 4.7kOhms
    # Remarks: The load resistance is broken into two parts: 3.12kOhms and 1.57kOhms for voltage division to 
    #          protect Raspberry Pi GPIO pins. Channel 0 measures the voltage across 1.57kOhms, which is approx. 1/3 
    #          of the total load resistance, VRL. Determine total load resistance for future calculations by multiplying
    #          channel 0 reading by 3 (approx 4.69/1.57). VRL is needed to determine Rs, since RL and Rs form another
    #          voltage divider, which future calculations are based on.
    ############################################################################   
        
    def read(self, channel = 0):                        # cmd1 and cmd2 are each 1 byte and serve as commands to instruct the MCP3008 where to read 
        cmd1 = 4 | 2 | ((channel & 4) >> 2)             # for channel = 0 = 0000 0000, cmd1 = 
        cmd2 = (channel & 3) << 6

        adc = self.spi.xfer2([cmd1, cmd2, 0])
        
        # FOR TESTING data = (((adc[1] & 15) << 6) | (adc[2]) & 63)   # data consists of integer values from 0 to 1023
        
        data = (((adc[1] & 15) << 8) | (adc[2]))        # data consists of integer values from 0 to 4095
                                                          
        return data
                            
    def close(self):
        self.spi.close()
