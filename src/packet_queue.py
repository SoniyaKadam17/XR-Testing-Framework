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


        # Insert packet into queue
        self.queue.append(packet)



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


                delivered_packets.append(
                    self.queue.popleft()
                )


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