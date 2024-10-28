from psychopy import core, logging
import serial
import time
from psychopy import sound
import numpy as np


class speaker_controller:
    def __init__(self, numSpeakers=16):
        self.serialPort = 'COM5'  # Change this to your actual COM port
        self.baudRate = 115200

        try:
            arduino = serial.Serial(self.serialPort, self.baudRate, timeout=1)
            time.sleep(0.5)  # Allow some time for the connection to establish
        except Exception as e:
            logging.error(f"Failed to connect to Arduino on {self.serialPort}: {str(e)}")
            core.quit()

        self.arduino = arduino
    
    def turn_on_speaker(self, speakerIndex):
        on_command = f"<1:{speakerIndex}>"
        self.arduino.write(on_command.encode())
        #time.sleep(0.1) # we will decide if we need time on main code

    def turn_off_speaker(self, speakerIndex):
        off_command = f"<0:{speakerIndex}>"
        self.arduino.write(off_command.encode())
        #time.sleep(0.1) # we will decide if we need time on main code
    def close_connection(self):
        self.arduino.close()
    def test_all_speakers(self):
        for i in range(1, 17):
            self.turn_on_speaker(i)
            time.sleep(0.1)
            self.turn_off_speaker(i)
            time.sleep(0.1)
        print("Tested all speakers")


# # Example usage
# speaker_controller = speaker_controller()
# speaker_controller.turn_on_speaker(1)
# speaker_controller.turn_off_speaker(1)

