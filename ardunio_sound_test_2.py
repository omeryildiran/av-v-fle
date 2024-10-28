import serial
import time

# Setup serial communication with Arduino
arduino = serial.Serial('COM5', 115200)
time.sleep(2)  # Allow time for the connection to establish

# Example sequence to test speakers
# We'll turn each speaker on and then off
speakers = range(1, 17)  # Speaker indices from 1 to 16

try:
    # Test each speaker
    for i in speakers:
        # Turn on speaker
        on_command = f"<1:{i}>"
        print("Sending:", on_command)
        arduino.write(on_command.encode())
        time.sleep(0.1)  # Short delay to observe the speaker being on

        # Turn off speaker
        off_command = f"<0:{i}>"
        print("Sending:", off_command)
        arduino.write(off_command.encode())
        time.sleep(0.1)  # Short delay before the next command
finally:
    arduino.close()  # Ensure to close the serial connection

print("Completed command sequence.")
