import random
import time

class TrackingSimulator:

    def generate_pose(self):

        return {
            "x": random.uniform(-1.0, 1.0),
            "y": random.uniform(-1.0, 1.0),
            "z": random.uniform(-1.0, 1.0),
            "pitch": random.uniform(-180, 180),
            "yaw": random.uniform(-180, 180),
            "roll": random.uniform(-180, 180),
            "timestamp": time.time()
        }