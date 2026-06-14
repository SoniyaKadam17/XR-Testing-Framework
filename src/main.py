import json
import asyncio
import csv
import time


from tracking import TrackingSimulator
from user_behavior import UserBehavior
from video_stream import VideoStream
from metrics import Metrics
from packet_generator import PacketGenerator


# NEW COMPONENT 2 IMPORTS
from impairment_config import ImpairmentConfig
from impairment_engine import NetworkImpairmentEngine



# ==========================================
# Load XR Profile
# ==========================================

with open("../profiles/high_load.json") as file:
    profile = json.load(file)



# ==========================================
# Initialize Components
# ==========================================

tracking = TrackingSimulator()

behavior = UserBehavior()

video = VideoStream()

metrics = Metrics()

packet_generator = PacketGenerator()



# ==========================================
# NETWORK IMPAIRMENT ENGINE
# ==========================================


network_config = ImpairmentConfig(

    latency_ms=50,

    jitter_ms=10,

    packet_loss_rate=0.02,

    bandwidth_mbps=50

)


network = NetworkImpairmentEngine(
    network_config
)



# ==========================================
# XR USER SIMULATION
# ==========================================

async def xr_user(user_id):


    start_time = time.time()


    fps = profile["fps"]

    frame_interval = 1 / fps



    while True:



        runtime = time.time() - start_time


        if runtime >= profile["session_duration"]:

            break



        # -----------------------------
        # Tracking
        # -----------------------------

        pose = tracking.generate_pose()



        # -----------------------------
        # User Event
        # -----------------------------

        event = behavior.generate_event()



        # -----------------------------
        # Generate XR Frame
        # -----------------------------

        frame = video.generate_frame()



        compressed_frame = video.compress_frame(
            frame
        )



        # -----------------------------
        # Traffic Scheduling
        # -----------------------------

        packet_size = profile["packet_size"]



        payload = compressed_frame[
            :packet_size
        ]



        # =================================================
        # COMPONENT 2 STARTS HERE
        # =================================================


        # Create XR packet object

        packet = {

            "user_id": user_id,

            "timestamp": time.time(),

            "size": packet_size,

            "payload": payload

        }



        # Send packet through impairment engine

        processed_packet = network.process_packet(
            packet
        )



        # Packet dropped

        if processed_packet is None:


            continue



        # Check packets that finished network delay

        delivered_packets = (
            network.get_delivered_packets()
        )



        for pkt in delivered_packets:


            metrics.increment_packets()


            metrics.add_bytes(
                pkt["size"]
            )
            # NEW:
            # Record real network latency

            metrics.add_latency(
                pkt["actual_latency_ms"]
            )


        # =================================================
        # COMPONENT 2 END
        # =================================================



        # -----------------------------
        # Existing Metrics
        # -----------------------------


        metrics.increment_frames()

        metrics.increment_events()



        await asyncio.sleep(
            frame_interval
        )





# ==========================================
# Metrics Display
# ==========================================

async def print_metrics():


    while True:


        metrics.print_metrics()


        print(
            network.get_statistics()
        )


        await asyncio.sleep(1)





# ==========================================
# CSV Logging
# ==========================================

async def log_metrics():


    with open(
        "../results/results.csv",
        "w",
        newline=""
    ) as file:


        writer = csv.writer(file)



        writer.writerow([

            "timestamp",

            "frames_sent",

            "events_generated",

            "packets_sent",

            "bytes_sent",

            "bandwidth_mbps",

            "avg_latency_ms",

            "min_latency_ms",

            "max_latency_ms",

            "network_dropped_packets",

            "network_loss_percentage"

        ])




        while True:



            stats = network.get_statistics()



            writer.writerow([

                time.time(),

                metrics.frames_sent,

                metrics.events_generated,

                metrics.packets_sent,

                metrics.bytes_sent,

                round(
                    metrics.get_bandwidth(),
                    3
                ),

                round(
                    metrics.get_average_latency(),
                    3
                ),

                round(
                    metrics.get_min_latency(),
                    3
                ),

                round(
                    metrics.get_max_latency(),
                    3
                ),


                stats["Dropped Packets"],

                stats["Packet Loss %"]

            ])



            file.flush()


            await asyncio.sleep(1)





# ==========================================
# Main Traffic Scheduler
# ==========================================

async def main():


    print("\n========== XR WORKLOAD ==========")


    print(
        f"Profile: {profile['name']}"
    )


    print(
        f"Users: {profile['users']}"
    )


    print(
        f"FPS: {profile['fps']}"
    )


    print(
        f"Packet Size: {profile['packet_size']} bytes"
    )


    print(
        "=================================\n"
    )



    tasks = []



    for user_id in range(
        profile["users"]
    ):


        tasks.append(

            asyncio.create_task(
                xr_user(user_id)
            )

        )



    tasks.append(

        asyncio.create_task(
            print_metrics()
        )

    )



    tasks.append(

        asyncio.create_task(
            log_metrics()
        )

    )



    await asyncio.gather(
        *tasks
    )




# ==========================================
# Start
# ==========================================

if __name__ == "__main__":


    try:

        asyncio.run(main())


    except KeyboardInterrupt:


        print(
            "\nSimulation stopped."
        )