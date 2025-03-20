import subprocess
import time
import random
from datetime import datetime

# Start server.py script in a separate process
server_process = subprocess.Popen(["python", "server.py"])

def generate_flight_path(start_lat, start_lon, grid_size, step_size):
    
    # Simulates a drone flying in a back-and-forth pattern to cover a 1km x 1km area. Returns a list of (lat, lon) tuples.
    
    path = []
    lat, lon = start_lat, start_lon
    direction = 1  # 1 for forward, -1 for backward

    for i in range(grid_size):
        for j in range(grid_size):
            path.append((lat, lon))
            lon += direction * step_size
        lat += step_size
        direction *= -1  # Reverse direction for next row
    
    return path

def write_random_numbers_to_file(filename, flight_path, min_val, max_val, delay):

    if min_val > max_val:
        print("Error: Minimum value cannot be greater than maximum value.")
        return

    try:
        with open(filename, 'w') as file:
            print(f"Writing sensor data to '{filename}'... Press Ctrl+C to stop.\n")
            
            for lat, lon in flight_path:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                random_number = f"{random.uniform(min_val, max_val):08.4f}"
                file.write(f"{timestamp}, {lat:.6f}, {lon:.6f}, {random_number}\n")
                file.flush()
                print(f"{timestamp}, Lat: {lat:.6f}, Lon: {lon:.6f}, Value: {random_number}")
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\nProcess stopped by user. Goodbye!")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    filename = "data.txt"
    start_lat = 37.7749  # Example starting latitude (San Francisco)
    start_lon = -122.4194  # Example starting longitude (San Francisco)
    grid_size = 20  # Steps in each direction - 22x22 square meter area
    step_size = 0.00001  # Approx. 1.1 meters per step
    min_val = float(0.0000)
    max_val = float(100.0000)
    delay = 2.0

    flight_path = generate_flight_path(start_lat, start_lon, grid_size, step_size)
    write_random_numbers_to_file(filename, flight_path, min_val, max_val, delay)
