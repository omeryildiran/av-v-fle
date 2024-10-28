from psychopy import core, logging
import serial
import time
from psychopy import sound
import numpy as np
# Setup
serialPort = 'COM5'  # Change this to your actual COM port
baudRate = 115200
try:
    arduino = serial.Serial(serialPort, baudRate, timeout=1)
    time.sleep(2)  # Allow some time for the connection to establish
except Exception as e:
    logging.error(f"Failed to connect to Arduino on {serialPort}: {str(e)}")
    core.quit()

numSpeakers = 22  # Total number of speakers

# initialize a sound object
# Define the number of speakers/channels
num_channels = 23

# Initialize a Sound object for each channel
tones = [sound.Sound('A', secs=0.1, stereo=True) for _ in range(num_channels)]

channels=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]  # Define the speaker
# channels 
channels=np.array(channels)
channels=np.repeat(channels, 1)

# Experiment routine
try:
    for i in channels:
        tone=tones[i]
        speakerIndex = str(i)  # Convert integer to string for sending

       # arduino.write(speakerIndex.encode())  # Send the speaker index as a byte
        
        # play sound on the specified speaker
        # tone.setSound('A', secs=0.2)  # Set frequency to 440 Hz for example, and duration
        # if i % 2 == 1:
        #     tone.setVolume(0.3)
        # else:
        #     tone.setVolume(1)
        # tone.play()  # Play the tone
                # Turn on speaker
        on_command = f"<1:{i}>"
        print("Sending:", on_command)
        arduino.write(on_command.encode())
        time.sleep(0.1)  # Short delay to observe the speaker being on

        tone.setSound('A', secs=0.3)
        tone.play()
        core.wait(0.2)
        # Turn off speaker
        off_command = f"<0:{i}>"
        print("Sending:", off_command)
        arduino.write(off_command.encode())
        time.sleep(0.1)  # Short delay before the next command

        print(f"Triggered speaker {i}")
finally:
    arduino.close()  # Make sure to close the serial connection

# End of the experiment
logging.info("Experiment completed successfully.")

