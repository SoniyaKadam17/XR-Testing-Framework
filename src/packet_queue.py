"""
Packet Queue Simulator

Simulates network buffering and delayed packet delivery.

Used by NetworkImpairmentEngine to model:
- Network propagation delay
- Queue waiting time
- Packet delivery timing
"""


import time
from collections import deque



class PacketQueue:


    def __init__(self):

        # Stores packets waiting for delivery
        self.queue = deque()

        # =====================================
        # Component 3: Queue Statistics
        # =====================================

        self.max_queue_size = 0
        self.total_queue_size = 0
        self.queue_samples = 0

        self.total_wait_time = 0
        self.wait_samples = 0



    def add_packet(self, packet, delivery_time):

        """
        Add packet into network queue.

        packet:
            XR packet dictionary

        delivery_time:
            Future timestamp when packet should arrive
        """

        # Add delivery timestamp to packet
        packet["delivery_time"] = delivery_time

        # =====================================
        # Component 3
        # Store queue entry time
        # =====================================

        packet["queue_entry_time"] = time.time()

        # Insert packet into queue
        self.queue.append(packet)

        # =====================================
        # Component 3
        # Queue statistics
        # =====================================

        current_size = len(self.queue)

        self.total_queue_size += current_size
        self.queue_samples += 1

        if current_size > self.max_queue_size:
            self.max_queue_size = current_size



    def get_ready_packets(self):

        """
        Return packets whose network delay has completed.

        Packets are released when:

        current_time >= delivery_time
        """

        current_time = time.time()

        delivered_packets = []

        while self.queue:

            packet = self.queue[0]

            # Packet delay completed
            if packet["delivery_time"] <= current_time:

                packet = self.queue.popleft()

                # =====================================
                # Component 3
                # Queue wait time
                # =====================================

                wait_time = (
                    current_time -
                    packet["queue_entry_time"]
                ) * 1000

                self.total_wait_time += wait_time
                self.wait_samples += 1

                delivered_packets.append(packet)

            else:

                # Queue is ordered by insertion time,
                # so remaining packets are not ready yet

                break

        return delivered_packets



    def size(self):

        """
        Return number of packets currently waiting.
        """

        return len(self.queue)



    def clear(self):

        """
        Empty the network queue.
        """

        self.queue.clear()



    # =====================================
    # Component 3 Statistics
    # =====================================

    def average_queue_size(self):

        if self.queue_samples == 0:
            return 0

        return (
            self.total_queue_size
            /
            self.queue_samples
        )


    def average_wait_time(self):

        if self.wait_samples == 0:
            return 0

        return (
            self.total_wait_time
            /
            self.wait_samples
        )


    def get_queue_statistics(self):

        return {

            "Current Queue Size": self.size(),

            "Average Queue Size": round(
                self.average_queue_size(),
                2
            ),

            "Maximum Queue Size": self.max_queue_size,

            "Average Queue Wait (ms)": round(
                self.average_wait_time(),
                2
            )
        }