import time


class Metrics:

    def __init__(self):

        self.frames_sent = 0
        self.events_generated = 0
        self.packets_sent = 0
        self.bytes_sent = 0

        self.start_time = time.time()



    # ==========================
    # Frame Counter
    # ==========================

    def increment_frames(self):

        self.frames_sent += 1



    # ==========================
    # Event Counter
    # ==========================

    def increment_events(self):

        self.events_generated += 1



    # ==========================
    # Packet Counter
    # ==========================

    def increment_packets(self):

        self.packets_sent += 1



    # ==========================
    # Byte Counter
    # ==========================

    def add_bytes(self, size):

        self.bytes_sent += size



    # ==========================
    # Bandwidth Calculation
    # ==========================

    def get_bandwidth(self):

        elapsed_time = time.time() - self.start_time


        if elapsed_time <= 0:

            return 0


        bits = self.bytes_sent * 8


        bandwidth_bps = bits / elapsed_time


        bandwidth_mbps = bandwidth_bps / 1_000_000


        return bandwidth_mbps



    # ==========================
    # Display Metrics
    # ==========================

    def print_metrics(self):

        runtime = time.time() - self.start_time


        print("\n========== METRICS ==========")

        print(
            f"Frames Sent: {self.frames_sent}"
        )

        print(
            f"Events Generated: {self.events_generated}"
        )

        print(
            f"Packets Sent: {self.packets_sent}"
        )

        print(
            f"Bytes Sent: {self.bytes_sent}"
        )

        print(
            f"Bandwidth: {self.get_bandwidth():.3f} Mbps"
        )

        print(
            f"Runtime: {runtime:.2f} seconds"
        )

        print("=============================\n")