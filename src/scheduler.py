import time

class Scheduler:

    def __init__(self):
        self.running = False

    def start(self):

        self.running = True

    def stop(self):

        self.running = False

    def wait(self, seconds):

        time.sleep(seconds)