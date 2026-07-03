import time
import csv
import os


class Metrics:


    def __init__(self):

        # -----------------------------
        # Counters
        # -----------------------------

        self.frames_sent = 0
        self.events_generated = 0
        self.packets_sent = 0
        self.bytes_sent = 0


        # -----------------------------
        # Latency storage
        # -----------------------------

        self.latencies = []


        # -----------------------------
        # Runtime
        # -----------------------------

        self.start_time = time.time()



    # =============================
    # Counter Functions
    # =============================


    def increment_frames(self):

        self.frames_sent += 1



    def increment_events(self):

        self.events_generated += 1



    def increment_packets(self):

        self.packets_sent += 1



    def add_bytes(self, size):

        self.bytes_sent += size



    # =============================
    # Latency Functions
    # =============================


    def add_latency(self, latency):

        # latency is stored in seconds
        self.latencies.append(latency)



    def get_average_latency(self):

        if len(self.latencies) == 0:
            return 0


        return (
            sum(self.latencies)
            /
            len(self.latencies)
        )



    def get_min_latency(self):

        if len(self.latencies) == 0:
            return 0


        return min(self.latencies)



    def get_max_latency(self):

        if len(self.latencies) == 0:
            return 0


        return max(self.latencies)



    # =============================
    # Bandwidth
    # =============================


    def get_bandwidth(self):

        runtime = self.get_runtime()


        if runtime <= 0:

            return 0


        bits = self.bytes_sent * 8


        return (
            bits / runtime
        ) / 1000000



    # =============================
    # Runtime
    # =============================


    def get_runtime(self):

        return (
            time.time()
            -
            self.start_time
        )



    # =============================
    # CSV Logging
    # =============================


    def write_csv(self, filename):

        file_exists = os.path.isfile(filename)


        with open(filename, "a", newline="") as file:


            writer = csv.writer(file)


            if not file_exists:

                writer.writerow(
                    [
                        "timestamp",
                        "frames_sent",
                        "events_generated",
                        "packets_sent",
                        "bytes_sent",
                        "bandwidth_mbps",
                        "avg_latency_ms",
                        "min_latency_ms",
                        "max_latency_ms"
                    ]
                )


            writer.writerow(
                [
                    time.time(),
                    self.frames_sent,
                    self.events_generated,
                    self.packets_sent,
                    self.bytes_sent,
                    round(
                        self.get_bandwidth(),
                        3
                    ),
                    round(
                       self.get_average_latency(),
                        3
                    ),

                    round(
                        self.get_min_latency(),
                        3
                    ),

                    round(
                        self.get_max_latency(),
                        3
                    )
                ]
                )



    # =============================
    # Console Output
    # =============================


    def print_metrics(self):


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
            f"Runtime: {self.get_runtime():.2f} seconds"
        )


        print("=============================\n")