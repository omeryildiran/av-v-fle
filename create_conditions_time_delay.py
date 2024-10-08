import numpy as np

class TimingGenerator:
    def __init__(self, trial_per_condition=12):
        self.trial_per_condition = trial_per_condition
        self.audio_delays = [-10, -6, -4, -2, 0, 2, 4, 6, 10]
        self.visual_delays = [-4, -2, -1, 0, 1, 2, 4]

    def generate_audio_visual_delays(self):
        audio_visual_delays = []
        # Create all possible combinations of audio and visual delays
        for audio_delay in self.audio_delays:
            for visual_delay in self.visual_delays:
                audio_visual_delays.append((audio_delay, visual_delay))

        # Extend the list by repeating it trial_per_condition times
        audio_visual_delays = np.tile(audio_visual_delays, self.trial_per_condition)

        # Create a matrix of audio_visual_delays
        audio_visual_delays = np.array(audio_visual_delays)
        sh = audio_visual_delays.shape
        dims = (sh[0] * sh[1]) // 2

        # Reshape it to create a matrix of mx2
        audio_visual_delays = audio_visual_delays.reshape(dims, 2)

        # Shuffle the matrix but keep the audio and visual delays together
        np.random.shuffle(audio_visual_delays)

        audioDelay = audio_visual_delays[:, 0]
        visualDelay = audio_visual_delays[:, 1]
        return audioDelay, visualDelay

    def generate_incident_times(self):
        audioDelay, visualDelay = self.generate_audio_visual_delays()
        trial_num = len(audioDelay)
        incident_times = np.random.uniform(250, 1050, trial_num * 2)
        return incident_times
    
    #random integers of -1 or +1 as length of incident_times uniformly
    def initial_bar_side(self):
        return np.random.choice([-1, 1], len(self.generate_incident_times()))
    
# # Create an instance of the TimingGenerator class
# timing_generator = TimingGenerator()
# audioDelay, visualDelay = timing_generator.generate_audio_visual_delays()
# incident_times = timing_generator.generate_incident_times()
# response = timing_generator.initial_bar_side()
# print(response[:50])