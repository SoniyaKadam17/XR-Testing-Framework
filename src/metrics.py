import time


class Metrics:


    def __init__(self):

        self.frames_sent = 0

        self.events_generated = 0

        self.packets_sent = 0

        self.bytes_sent = 0


        # Latency storage

        self.latencies = []


        self.start_time = time.time()



    # -----------------------------
    # Counters
    # -----------------------------

    def increment_frames(self):

        self.frames_sent += 1



    def increment_events(self):

        self.events_generated += 1



    def increment_packets(self):

        self.packets_sent += 1



    def add_bytes(self, size):

        self.bytes_sent += size



    # -----------------------------
    # Latency
    # -----------------------------

    def add_latency(self, latency):

        self.latencies.append(
            latency
        )



    def get_average_latency(self):

        if len(self.latencies) == 0:

            return 0


        return (
            sum(self.latencies)
            /
            len(self.latencies)
        ) * 1000



    def get_min_latency(self):

        if len(self.latencies)==0:

            return 0


        return min(
            self.latencies
        ) * 1000



    def get_max_latency(self):

        if len(self.latencies)==0:

            return 0


        return max(
            self.latencies
        ) * 1000



    # -----------------------------
    # Bandwidth
    # -----------------------------

    def get_bandwidth(self):

        runtime = (
            time.time()
            -
            self.start_time
        )


        if runtime <=0:

            return 0


        bits = self.bytes_sent * 8


        return (
            bits/runtime
        )/1000000



    # -----------------------------
    # Print Metrics
    # -----------------------------

    def print_metrics(self):


        runtime = (
            time.time()
            -
            self.start_time
        )


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
            f"Average Latency: {self.get_average_latency():.2f} ms"
        )


        print(
            f"Min Latency: {self.get_min_latency():.2f} ms"
        )


        print(
            f"Max Latency: {self.get_max_latency():.2f} ms"
        )


        print(
            f"Runtime: {runtime:.2f} seconds"
        )

        print("=============================\n")