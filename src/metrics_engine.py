"""
Metrics Collection Engine

Centralized metrics collector for the XR Testing Framework.

This module gathers statistics from every component:

• XR Workload Generator
• Network Impairment Engine
• Packet Queue
• Scheduler

It provides one unified interface for the experiment.
"""

import time


class MetricsEngine:

    def __init__(self):

        # ====================================
        # Experiment Timing
        # ====================================

        self.start_time = time.time()
        self.end_time = None

        # ====================================
        # Traffic Statistics
        # ====================================

        self.frames_sent = 0
        self.events_generated = 0

        self.total_packets = 0
        self.delivered_packets = 0
        self.dropped_packets = 0

        self.bytes_sent = 0

        # ====================================
        # Latency Statistics
        # ====================================

        self.latencies = []

        # ====================================
        # Queue Statistics
        # ====================================

        self.queue_sizes = []
        self.queue_wait_times = []



    # ====================================
    # Experiment
    # ====================================

    def finish(self):

        self.end_time = time.time()



    def runtime(self):

        if self.end_time is None:

            return time.time() - self.start_time

        return self.end_time - self.start_time



    # ====================================
    # Frame Statistics
    # ====================================

    def record_frame(self):

        self.frames_sent += 1



    def record_event(self):

        self.events_generated += 1



    # ====================================
    # Packet Statistics
    # ====================================

    def record_packet_generated(self):

        self.total_packets += 1



    def record_packet_delivered(self):

        self.delivered_packets += 1



    def record_packet_dropped(self):

        self.dropped_packets += 1



    def record_bytes(self, size):

        self.bytes_sent += size



    # ====================================
    # Latency
    # ====================================

    def record_latency(self, latency_ms):

        self.latencies.append(latency_ms)



    def average_latency(self):

        if not self.latencies:

            return 0

        return sum(self.latencies) / len(self.latencies)



    def minimum_latency(self):

        if not self.latencies:

            return 0

        return min(self.latencies)



    def maximum_latency(self):

        if not self.latencies:

            return 0

        return max(self.latencies)



    # ====================================
    # Jitter
    # ====================================

    def average_jitter(self):

        if len(self.latencies) < 2:

            return 0

        differences = []

        previous = self.latencies[0]

        for latency in self.latencies[1:]:

            differences.append(abs(latency - previous))
            previous = latency

        return sum(differences) / len(differences)



    # ====================================
    # Queue Statistics
    # ====================================

    def record_queue_size(self, size):

        self.queue_sizes.append(size)



    def average_queue_size(self):

        if not self.queue_sizes:

            return 0

        return sum(self.queue_sizes) / len(self.queue_sizes)



    def maximum_queue_size(self):

        if not self.queue_sizes:

            return 0

        return max(self.queue_sizes)



    def record_queue_wait(self, wait_ms):

        self.queue_wait_times.append(wait_ms)



    def average_queue_wait(self):

        if not self.queue_wait_times:

            return 0

        return sum(self.queue_wait_times) / len(self.queue_wait_times)



    # ====================================
    # Throughput
    # ====================================

    def throughput(self):

        runtime = self.runtime()

        if runtime <= 0:

            return 0

        bits = self.bytes_sent * 8

        return (bits / runtime) / 1_000_000



    # ====================================
    # Delivery Ratio
    # ====================================

    def delivery_ratio(self):

        if self.total_packets == 0:

            return 0

        return (

            self.delivered_packets
            /
            self.total_packets

        ) * 100



    # ====================================
    # Packet Loss
    # ====================================

    def packet_loss(self):

        if self.total_packets == 0:

            return 0

        return (

            self.dropped_packets
            /
            self.total_packets

        ) * 100



    # ====================================
    # Summary
    # ====================================

    def summary(self):

        return {

            "Frames Sent":
                self.frames_sent,

            "Events Generated":
                self.events_generated,

            "Total Packets":
                self.total_packets,

            "Delivered Packets":
                self.delivered_packets,

            "Dropped Packets":
                self.dropped_packets,

            "Packet Loss %":
                round(
                    self.packet_loss(),
                    2
                ),

            "Delivery Ratio %":
                round(
                    self.delivery_ratio(),
                    2
                ),

            "Bytes Sent":
                self.bytes_sent,

            "Average Latency":
                round(
                    self.average_latency(),
                    2
                ),

            "Minimum Latency":
                round(
                    self.minimum_latency(),
                    2
                ),

            "Maximum Latency":
                round(
                    self.maximum_latency(),
                    2
                ),

            "Average Jitter":
                round(
                    self.average_jitter(),
                    2
                ),

            "Average Queue Size":
                round(
                    self.average_queue_size(),
                    2
                ),

            "Maximum Queue Size":
                self.maximum_queue_size(),

            "Average Queue Wait":
                round(
                    self.average_queue_wait(),
                    2
                ),

            "Throughput":
                round(
                    self.throughput(),
                    3
                ),

            "Runtime":
                round(
                    self.runtime(),
                    2
                )
        }