import RPi.GPIO as GPIO
import time

# Setup GPIO once at the start
GPIO.setmode(GPIO.BCM)
MOTOR_PIN = 18 # GPIO pin 18, corresponds to physical pin 12 (6th pin down on the righthand side, 4 pins lower than the 5v output)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def motor_control(pin, duration, state="on"):
    """
    Controls the motor by turning it ON or OFF for a specified duration.
    
    Args:
        pin (int): The GPIO pin connected to the transistor's gate/base.
        duration (float): How long (in seconds) to keep the motor running.
        state (str): "on" to run motor, "off" to stop motor.
    """
    if state.lower() == "on":
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(pin, GPIO.LOW)
    elif state.lower() == "off":
        GPIO.output(pin, GPIO.LOW)
        time.sleep(duration)
    else:
        print(f"Invalid state '{state}'. Use 'on' or 'off'. Skipping...")

# Example usage:
if __name__ == "__main__":
    try:
        while True:
            motor_control(MOTOR_PIN, 2, "on")  # Motor ON for 2 seconds
            time.sleep(1)                     # Pause 5 seconds to let sensor respond

    except KeyboardInterrupt:
        print("\n Interrupted")