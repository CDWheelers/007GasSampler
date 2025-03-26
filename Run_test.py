import subprocess
import time
from datetime import datetime

# Start server.py script in a separate process
server_process = subprocess.Popen(["python", "server.py"])

def generate_flight_path(start_lat, start_lon, grid_size, step_size):
    """
    Simulates a drone flying in a back-and-forth pattern to cover a 1km x 1km area.
    Returns a list of (lat, lon) tuples.
    """
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

def write_sensor_data(filename, flight_path, initial_value, decrement, delay):
    """
    Writes GPS coordinates and sensor values to a file.
    """
    try:
        with open(filename, 'w') as file:
            print(f"Writing sensor data to '{filename}'... Press Ctrl+C to stop.\n")
            count = 0
            sensor_value = initial_value
            
            for lat, lon in flight_path:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                file.write(f"{timestamp}, {lat:.6f}, {lon:.6f}, {sensor_value:.4f}\n")
                file.flush()
                print(f"{timestamp} - Lat: {lat:.6f}, Lon: {lon:.6f}, Value: {sensor_value:.4f}")
                sensor_value -= decrement
                count += 1
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\nProcess stopped by user. Goodbye!")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    filename = "data.txt"
    start_lat = 37.7749  # Example starting latitude (San Francisco)
    start_lon = -122.4194  # Example starting longitude (San Francisco)
    grid_size = 10  # 10x10 grid
    step_size = 0.0001  # Approx. 11 meters per step
    initial_value = 100.0
    decrement = 0.2
    delay = 0.1

    flight_path = generate_flight_path(start_lat, start_lon, grid_size, step_size)
    write_sensor_data(filename, flight_path, initial_value, decrement, delay)
