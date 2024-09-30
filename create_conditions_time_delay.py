import numpy as np

class TimingGenerator:
    def __init__(self, trial_per_condition=12):
        self.trial_per_condition = trial_per_condition
        self.audio_delays = [-10, -6, -4, -2, 0, 2, 4, 6, 10]
        self.visual_delays = [-4, -2, -1, 0, 1, 2, 4]
        self.audio_visual_delays = []
        self.onset_flash_times = []

    def generate_audio_visual_delays(self):
        # Create all possible combinations of audio and visual delays
        for audio_delay in self.audio_delays:
            for visual_delay in self.visual_delays:
                self.audio_visual_delays.append((audio_delay, visual_delay))

        # Extend the list by repeating it trial_per_condition times
        self.audio_visual_delays = np.tile(self.audio_visual_delays, self.trial_per_condition)

        # Create a matrix of audio_visual_delays
        self.audio_visual_delays = np.array(self.audio_visual_delays)
        sh = self.audio_visual_delays.shape
        dims = (sh[0] * sh[1]) // 2

        # Reshape it to create a matrix of mx2
        self.audio_visual_delays = self.audio_visual_delays.reshape(dims, 2)

        # Shuffle the matrix but keep the audio and visual delays together
        np.random.shuffle(self.audio_visual_delays)

        audioDelay= self.audio_visual_delays[:, 0]
        visualDelay = self.audio_visual_delays[:, 1]
        return audioDelay, visualDelay

    def generate_onset_flash_times(self):
        trial_num = len(self.audio_visual_delays)
        self.onset_flash_times = np.random.uniform(300, 900, trial_num * 2)
        return self.onset_flash_times

# Example usage
# delay_generator = TimingGenerator()
# audio_visual_delays = delay_generator.generate_audio_visual_delays()
# onset_flash_times = delay_generator.generate_onset_flash_times()

# print("Audio Visual Delays:", audio_visual_delays)
# print("Onset Flash Times:", onset_flash_times)