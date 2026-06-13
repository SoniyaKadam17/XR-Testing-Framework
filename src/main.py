import json
import asyncio
import csv
import time


from tracking import TrackingSimulator
from user_behavior import UserBehavior
from video_stream import VideoStream
from metrics import Metrics
from packet_generator import PacketGenerator



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
# XR USER SIMULATION
# ==========================================

async def xr_user(user_id):


    start_time = time.time()


    fps = profile["fps"]

    frame_interval = 1 / fps



    while True:


        # -----------------------------
        # Session Duration Check
        # -----------------------------

        runtime = time.time() - start_time


        if runtime >= profile["session_duration"]:

            break



        # -----------------------------
        # Tracking Data
        # -----------------------------

        pose = tracking.generate_pose()



        # -----------------------------
        # User Interaction
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



        # -----------------------------
        # Packet Transmission
        # -----------------------------

        latency = await packet_generator.send_packet(payload)
        metrics.add_latency(latency)



        # -----------------------------
        # Update Metrics
        # -----------------------------

        metrics.increment_frames()

        metrics.increment_events()

        metrics.increment_packets()

        metrics.add_bytes(
            packet_size
        )



        # -----------------------------
        # Maintain XR FPS
        # -----------------------------

        await asyncio.sleep(
            frame_interval
        )



# ==========================================
# Metrics Display
# ==========================================

async def print_metrics():


    while True:


        metrics.print_metrics()


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

        # header (UPDATED)
        writer.writerow([
            "timestamp",
            "frames_sent",
            "events_generated",
            "packets_sent",
            "bytes_sent",
            "bandwidth_mbps",
            "avg_latency_ms"
        ])

        while True:

            # compute latency here
            avg = metrics.get_average_latency()

            writer.writerow([
                time.time(),
                metrics.frames_sent,
                metrics.events_generated,
                metrics.packets_sent,
                metrics.bytes_sent,
                round(metrics.get_bandwidth(), 3),
                round(avg, 3)
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
        f"Tracking Rate: {profile['tracking_rate']} Hz"
    )


    print(
        f"Target Bitrate: {profile['bitrate_mbps']} Mbps"
    )


    print(
        "=================================\n"
    )



    tasks = []



    # ----------------------------------
    # Create XR Users
    # ----------------------------------

    for user_id in range(
        profile["users"]
    ):


        task = asyncio.create_task(

            xr_user(user_id)

        )


        tasks.append(task)



    # ----------------------------------
    # Background Monitoring
    # ----------------------------------

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
# Program Start
# ==========================================

if __name__ == "__main__":


    try:


        asyncio.run(main())


    except KeyboardInterrupt:


        print(
            "\nSimulation stopped."
        )