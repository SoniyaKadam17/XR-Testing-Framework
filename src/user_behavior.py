import random
import time

XR_EVENTS = [
    "HEAD_MOVE",
    "HAND_MOVE",
    "GRAB_OBJECT",
    "RELEASE_OBJECT",
    "MENU_CLICK",
    "TELEPORT"
]

class UserBehavior:

    def generate_event(self):
        return {
            "event": random.choice(XR_EVENTS),
            "timestamp": time.time()
        }