import subprocess
import time
from datetime import datetime
from pymavlink import mavutil

# ------------------------------------------------------------------------------------------------------------------------------
# GPS FETCHING FUNCTION
# ----------------------------------------------------------------------------------------------------------------------------------
def get_gps_data(serial_port="COM8", baud_rate=57600):
    print(f"Connecting to Pixhawk on {serial_port} at {baud_rate} baud...")
    try:
        master = mavutil.mavlink_connection(serial_port, baud=baud_rate)
        master.wait_heartbeat(timeout=10)
        print("Connected to Pixhawk! Heartbeat received.")
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        return None, None

    print("Waiting for GLOBAL_POSITION_INT message...\n")

    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if not msg:
            print("No GPS data received. Retrying...")
            continue

        lat = msg.lat / 1e7
        lon = msg.lon / 1e7

        print(f"Latitude: {lat:.7f}, Longitude: {lon:.7f}")
        return lat, lon

# --------------------------------------------------------------------------------------------------------------------------------
# SENSOR DATA WRITER
# --------------------------------------------------------------------------------------------------------------------------------
def write_sensor_data(filename, initial_value, decrement, delay):
    try:
        with open(filename, 'a') as file:
            print(f"Writing sensor data to '{filename}'... Press Ctrl+C to stop.\n")

            sensor_value = initial_value
            
            while True:
                lat, lon = get_gps_data()

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

                file.write(f"{timestamp}, {lat:.6f}, {lon:.6f}, {sensor_value:.4f}\n")
                file.flush()
                
                print(f"{timestamp} - Lat: {lat:.6f}, Lon: {lon:.6f}, Value: {sensor_value:.4f}")

                sensor_value -= decrement

                time.sleep(delay)
    except KeyboardInterrupt:
        print("\nProcess stopped by user.")
    except Exception as e:
        print(f"Error writing to file: {e}")

# ---------------------------------------------------------------------------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Start background server 
    try:
        server_process = subprocess.Popen(["python", "server.py"])
    except Exception as e:
        print(f"Warning: Could not start server.py — {e}")

    # Define parameters and generate path
    filename = "data.txt"
    grid_size = 10
    initial_value = 100.0
    decrement = 0.2
    delay = 0.1

    # Write sensor data along the path
    write_sensor_data(filename, initial_value, decrement, delay)
