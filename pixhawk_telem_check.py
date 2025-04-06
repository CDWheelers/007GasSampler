import time
from pymavlink import mavutil

serial_port = "/dev/serial0"
baud_rate = 57600

print(f"Connecting to Pixhawk on {serial_port} at {baud_rate} baud...")

try:
    master = mavutil.mavlink_connection(serial_port, baud=baud_rate)
    print("Waiting for heartbeat from Pixhawk...")
    master.wait_heartbeat(timeout=10)

    print("\n Connection successful!")
    print(f"System ID: {master.target_system}, Component ID: {master.target_component}")

    print("Sending ping...")
    master.mav.ping_send(
        int(time.time() * 1e6),
        0, 0,
        0
    )

except Exception as e:
    print(f"\n Connection failed: {e}")