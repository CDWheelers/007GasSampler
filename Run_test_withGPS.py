import random
import time
from datetime import datetime

def write_random_numbers_to_file(filename, NH3_min, NH3_max, NH3_decimal_places, GPS_min, GPS_max, delay):

    """
    Writes a specified number of random integers to a file.

    Args:
        filename (str): The name of the file to write to.
        min_val (float)): The minimum value for the random numbers.
        max_val (float): The maximum value for the random numbers.
        delay (float)): Time delay in seconds between each entry being written to the file.
        decimal_places(int): number of decimal places the generated random numbers will have.
    """   
    try:
    
        with open(filename, 'w') as file: #'w' overwrites file of same filename, 'a' appends
            print(f"Writing random numbers to '{filename}'... Press Ctrl+C to stop.\n")
            
            count = 1  # keep track of how many numbers have been written
            while True:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4] #get current timestamp
                random_NH3 = round(random.uniform(NH3_min, NH3_max), NH3_decimal_places)
                random_GPS = random.uniform(GPS_min, GPS_max)

                file.write(f"{timestamp} - {random_NH3} - {random_GPS}\n")
                file.flush()  # ensure immediate writing to the file from program buffer
                print(f"Written {count}: {random_NH3} ppm at {timestamp}")
                count += 1
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\nProcess stopped by user. Goodbye!")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    filename = datetime.now().strftime("random_numbers_%Y-%m-%d_%H-%M-%S.txt") #creates new file with date and time in filename
    NH3_min = float(0.0000)
    NH3_max = float(10.0000)
    NH3_decimal_places = int(4)

    GPS_min = float(20.0000)
    GPS_max = float(30.0000)

    delay = float(2.0000)
    
    write_random_numbers_to_file(filename, NH3_min, NH3_max, NH3_decimal_places, GPS_min, GPS_max, delay)