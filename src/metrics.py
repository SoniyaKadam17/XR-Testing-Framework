class Metrics:

    def __init__(self):

        self.frames_sent = 0
        self.events_generated = 0
        self.packets_sent = 0

    def increment_frames(self):
        self.frames_sent += 1

    def increment_events(self):
        self.events_generated += 1

    def increment_packets(self):
        self.packets_sent += 1