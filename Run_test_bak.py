import random
import time

def write_random_numbers_to_file(filename, num_numbers, min_val, max_val, delay):

    """
    Writes a specified number of random integers to a file.

    Args:
        filename (str): The name of the file to write to.
        num_numbers (int): The number of random numbers to generate.
        min_val (int): The minimum value for the random numbers.
        max_val (int): The maximum value for the random numbers.
        delay (int): Time delay in seconds between each entry being written to the file.
    """
# file.flush() ensures numbers are immediately sent from program's buffer to physical file on disk, allowing each number to be written one at a time.

    with open(filename, 'w') as file:
        for _ in range(num_numbers):
            random_number = random.randint(min_val, max_val)
            file.write(str(random_number) + '\n')
            file.flush()
            time.sleep(delay)

if __name__ == "__main__":
    filename = "random_numbers.txt"
    
    num_numbers = 100
    min_val = 1
    max_val = 100
    delay = 1

    write_random_numbers_to_file(filename, num_numbers, min_val, max_val, delay)
    print(f"{num_numbers} random numbers written to '{filename}'.")