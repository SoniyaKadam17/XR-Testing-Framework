"""
Network impairment configuration.

Defines the network conditions used for XR testing experiments.
"""


class ImpairmentConfig:

    def __init__(
        self,
        latency_ms=20,
        jitter_ms=5,
        packet_loss_rate=0.01,
        bandwidth_mbps=50
    ):

        # Base network delay
        self.latency_ms = latency_ms

        # Variation in delay
        self.jitter_ms = jitter_ms

        # Probability of packet dropping
        # Example:
        # 0.01 = 1% packet loss
        self.packet_loss_rate = packet_loss_rate

        # Maximum available bandwidth
        self.bandwidth_mbps = bandwidth_mbps


    def display(self):

        print("===== Network Configuration =====")
        print(f"Latency: {self.latency_ms} ms")
        print(f"Jitter: ±{self.jitter_ms} ms")
        print(f"Packet Loss: {self.packet_loss_rate * 100}%")
        print(f"Bandwidth: {self.bandwidth_mbps} Mbps")
        print("=================================")