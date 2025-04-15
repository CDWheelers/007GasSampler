# Make sure that:
# UART is enabled on Pi (sudo raspi-config > Interface > Enable Serial Hardware)
# TELEM2 Connected to /dev/serial0 at 57600 baud
# pymavlink is installed (preferably inside a virtual environment) from previous ReadMe txt file

import time
from pymavlink import mavutil

# Change if using different port or baud
serial_port = "/dev/serial0"
baud_rate = 57600

def main():
    print(f"Connecting to Pixhawk on {serial_port} at {baud_rate} baud...")
    try:
        # Connect to Pixhawk via serial
        master = mavutil.mavlink_connection(serial_port, baud=baud_rate)
        master.wait_heartbeat(timeout=10)
        print("[OK] Connected to Pixhawk!")
    except Exception as e:
        print(f"[FAIL] Could not connect: {e}")
        return

    print("Waiting for GPS data...\n")

    while True:
        # Wait for a GPS_RAW_INT message
        msg = master.recv_match(type='GPS_RAW_INT', blocking=True, timeout=5)
        if not msg:
            print("No GPS data received. Retrying...")
            continue

        # Extract GPS information
        fix_type = msg.fix_type
        lat = msg.lat / 1e7  # Convert to degrees
        lon = msg.lon / 1e7
        alt = msg.alt / 1000.0  # Convert to meters

        # Fix types: 0-1 = No fix, 2 = 2D fix, 3 = 3D fix
        fix_desc = {
            0: "No GPS",
            1: "No Fix",
            2: "2D Fix",
            3: "3D Fix",
            4: "RTK Float",
            5: "RTK Fixed"
        }.get(fix_type, f"Unknown ({fix_type})")

        print(f"[{fix_desc}] Lat: {lat:.7f}, Lon: {lon:.7f}, Alt: {alt:.2f} m")
        time.sleep(1)

if __name__ == "__main__":
    main()
