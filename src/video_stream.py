import random


class VideoStream:


    def __init__(self):

        self.frame_id = 0



    def generate_frame(self):

        self.frame_id += 1

        # Simulated XR frame
        frame = {

            "frame_id": self.frame_id,

            "resolution": "4K",

            "codec": "H265"

        }


        return frame



    def compress_frame(self, frame):

        # Do NOT actually compress
        # Just simulate compressed XR data


        simulated_size = 5000


        return bytes(
            random.getrandbits(8)
            for _ in range(simulated_size)
        )