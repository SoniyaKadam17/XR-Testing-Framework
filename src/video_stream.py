import numpy as np
import zlib

class VideoStream:

    def generate_frame(self):

        frame = np.random.randint(
            0,
            255,
            (720, 1280, 3),
            dtype=np.uint8
        )

        return frame

    def compress_frame(self, frame):

        return zlib.compress(
            frame.tobytes()
        )