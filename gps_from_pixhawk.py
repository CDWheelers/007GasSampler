# Make sure that:
# UART is enabled on Pi (sudo raspi-config > Interface > Enable Serial Hardware)
# TELEM2 Connected to /dev/serial0 at 57600 baud
# pymavlink is installed (preferably inside a virtual environment) from previous ReadMe txt file

import time
from pymavlink import mavutil

# Change if using different port or baud
serial_port = "/dev/serial0"
baud_rate = 57600

def get_gps_data():
    print(f"Connecting to Pixhawk on {serial_port} at {baud_rate} baud...")
    try:
        # Connect to Pixhawk via serial
        master = mavutil.mavlink_connection(serial_port, baud=baud_rate)
        master.wait_heartbeat(timeout=10)
        print("Connected to Pixhawk!")
    except Exception as e:
        print(f"Could not connect: {e}")
        return None, None #Return None if connection fails

    print("Waiting for GPS data...\n")

    while True:
        # Wait for a GLOBAL_POSITION_INT message
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if not msg:
            print("No GPS data received. Retrying...")
            continue

        # Extract GPS information
        lat = msg.lat / 1e7  # Convert to degrees
        lon = msg.lon / 1e7

        return lat, lon

if __name__ == "__main__":
    lat, lon = get_gps_data()
    print(f"Latitude: {lat}, Longitude: {lon}")
