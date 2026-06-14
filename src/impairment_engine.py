"""
Network Impairment Engine

Simulates:
- Packet loss
- Latency
- Jitter
- Network delay queue

Also measures actual packet latency
and sends it back to metrics.
"""


import random
import time

from packet_queue import PacketQueue



class NetworkImpairmentEngine:


    def __init__(self, config):

        self.config = config

        self.packet_queue = PacketQueue()


        # Statistics

        self.total_packets = 0

        self.dropped_packets = 0

        self.delivered_packets = 0



    # =====================================
    # Packet Loss Model
    # =====================================

    def apply_packet_loss(self):

        probability = random.random()


        if probability < self.config.packet_loss_rate:

            return True


        return False



    # =====================================
    # Latency + Jitter Model
    # =====================================

    def calculate_delay(self):


        jitter = random.uniform(
            -self.config.jitter_ms,
            self.config.jitter_ms
        )


        delay = (
            self.config.latency_ms
            +
            jitter
        )


        return max(delay, 0)



    # =====================================
    # Process Incoming Packet
    # =====================================

    def process_packet(self, packet):


        self.total_packets += 1



        # -------------------------------
        # Packet Loss
        # -------------------------------

        if self.apply_packet_loss():


            self.dropped_packets += 1


            return None



        # -------------------------------
        # Calculate Network Delay
        # -------------------------------

        delay_ms = self.calculate_delay()



        send_time = time.time()


        delivery_time = (
            send_time
            +
            delay_ms / 1000
        )



        # Store network information

        packet["send_time"] = send_time

        packet["expected_latency_ms"] = delay_ms



        # Add to network queue

        self.packet_queue.add_packet(
            packet,
            delivery_time
        )


        return packet




    # =====================================
    # Release Delivered Packets
    # =====================================

    def get_delivered_packets(self):


        packets = (
            self.packet_queue.get_ready_packets()
        )


        for packet in packets:


            receive_time = time.time()


            actual_latency = (

                receive_time
                -
                packet["send_time"]

            ) * 1000



            packet["actual_latency_ms"] = (
                actual_latency
            )



            self.delivered_packets += 1



        return packets




    # =====================================
    # Statistics
    # =====================================

    def get_statistics(self):


        loss_percentage = 0



        if self.total_packets > 0:


            loss_percentage = (

                self.dropped_packets
                /
                self.total_packets

            ) * 100



        return {


            "Total Packets":
                self.total_packets,


            "Dropped Packets":
                self.dropped_packets,


            "Delivered Packets":
                self.delivered_packets,


            "Packet Loss %":
                round(
                    loss_percentage,
                    2
                )

        }