import asyncio
import time
import random

class PacketGenerator:


    def __init__(self):

        self.total_packets = 0
        self.latency_records = []



    async def send_packet(self, payload):


        self.total_packets += 1


        # -----------------------------
        # Timestamp before sending
        # -----------------------------

        send_time = time.time()



        # -----------------------------
        # Simulated XR Network Delay
        # 5ms - 30ms
        # -----------------------------

        network_delay = random.uniform(
            0.005,
            0.030
        )


        # Non-blocking wait
        await asyncio.sleep(
            network_delay
        )



        # -----------------------------
        # Timestamp after receiving
        # -----------------------------

        receive_time = time.time()



        latency = (
            receive_time -
            send_time
        )



        self.latency_records.append(
            latency
        )



        return latency