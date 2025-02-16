import serial
import time
from pynput.keyboard import Controller, Key

# Adjust these settings according to your environment
SERIAL_PORT = '/dev/ttyACM0'  # Windows example; for Linux/Mac, e.g., '/dev/ttyACM0'
BAUD_RATE = 9600

# Initialize serial connection and keyboard controller
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
keyboard = Controller()

# Mapping from sensor number to a specific key
sensor_key_mapping = {
    "0": 'z',
    "1": 'c',
    "2": 'e',
    "3": 'q',
    "4": 's'
}

def press_key(key):
    #print(f"Pressing {key}")
    keyboard.press(key)

def release_key(key):
    #print(f"Releasing {key}")
    keyboard.release(key)

def process_serial_line(line):
    # Expected message format: SENSOR_<num>_PRESSED or SENSOR_<num>_RELEASED
    if not line.startswith("SENSOR_"):
        return
    parts = line.split('_')
    if len(parts) != 3:
        return
    sensor_id = parts[1]
    action = parts[2].strip()  # remove newline

    if sensor_id in sensor_key_mapping:
        key = sensor_key_mapping[sensor_id]
        if action == "PRESSED":
            press_key(key)
        elif action == "RELEASED":
            release_key(key)

def main():
    # Give some time for the serial connection to initialize
    time.sleep(2)
    print("Listening for sensor events...")

    try:
        while True:
            if ser.in_waiting > 0:
                # Read a line from the serial port (ended with \n)
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print("Received:", line)
                    process_serial_line(line)
            else:
                time.sleep(0.01)  # small delay to reduce busy waiting

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
