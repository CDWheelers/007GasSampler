import subprocess
import random
import time
from datetime import datetime

# Start server.py script in a seperate process
server_process = subprocess.Popen(["python", "server.py"])

def write_random_numbers_to_file(filename, min_val, max_val, delay, decimal_places):

    """
    Writes a specified number of random integers to a file.

    Args:
        filename (str): The name of the file to write to.
        min_val (float)): The minimum value for the random numbers.
        max_val (float): The maximum value for the random numbers.
        delay (float)): Time delay in seconds between each entry being written to the file.
        decimal_places(int): number of decimal places the generated random numbers will have.
    """
    if min_val > max_val:
        print("Error: Minimum value cannot be greater than maximum value.")
        return
    
    try:
    
        with open(filename, 'w') as file: #'w' overwrites file of same filename, 'a' appends
            print(f"Writing random numbers to '{filename}'... Press Ctrl+C to stop.\n")
            
            count = 1  # Keep track of how many numbers have been written
            while True:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4] # Get current timestamp
                random_number = round(random.uniform(min_val, max_val), decimal_places)
                file.write(f"{timestamp} - {random_number}\n")
                file.flush()  # Ensure immediate writing to the file from program buffer
                print(f"Written {count}: {random_number} at {timestamp}")
                count += 1
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\nProcess stopped by user. Goodbye!")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    # filename = datetime.now().strftime("random_numbers_%Y-%m-%d_%H-%M-%S.txt") # Creates new file with date and time in filename
    filename = "data.txt" # For testing purposes
    min_val = float(0.0000)
    max_val = float(100.0000)
    delay = float(2.0000)
    decimal_places = int(4)

    write_random_numbers_to_file(filename, min_val, max_val, delay, decimal_places)


