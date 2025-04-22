import subprocess
import time
from datetime import datetime
from gps_from_pixhawk import get_gps_data

# Start server.py script in a separate process
server_process = subprocess.Popen(["python", "server.py"])

def write_sensor_data(filename, flight_path, initial_value, decrement, delay):
    """
    Writes GPS coordinates and sensor values to a file.
    """
    try:
        with open(filename, 'a') as file:
            print(f"Writing sensor data to '{filename}'... Press Ctrl+C to stop.\n")
            count = 0
            sensor_value = initial_value
            
            while True:
                lat, lon = get_gps_data()

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
    initial_value = 1000.0
    decrement = 0.1
    delay = 0.1

write_sensor_data(filename, initial_value, decrement, delay)
