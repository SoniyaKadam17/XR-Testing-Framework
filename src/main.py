import json
import asyncio
import csv
import time

from tracking import TrackingSimulator
from user_behavior import UserBehavior
from video_stream import VideoStream
from metrics import Metrics
from packet_generator import PacketGenerator


# Load workload profile
with open("../profiles/low_load.json") as f:
    profile = json.load(f)


tracking = TrackingSimulator()
behavior = UserBehavior()
video = VideoStream()
metrics = Metrics()
packet_generator = PacketGenerator()


async def xr_user(user_id):
    """
    Simulates one XR user continuously.
    """

    while True:

        # Generate tracking data
        pose = tracking.generate_pose()

        # Generate user event
        event = behavior.generate_event()

        # Generate video frame
        frame = video.generate_frame()

        # Compress frame
        compressed = video.compress_frame(frame)

        # Send first 1024 bytes as network traffic
        packet_generator.send_packet(
            compressed[:1024]
        )

        # Update metrics
        metrics.increment_frames()
        metrics.increment_events()
        metrics.increment_packets()

        # Simulate 90 Hz XR updates
        await asyncio.sleep(1 / 90)


async def print_metrics():
    """
    Display metrics every second.
    """

    while True:

        print("\n========== METRICS ==========")
        print(f"Frames Sent: {metrics.frames_sent}")
        print(f"Events Generated: {metrics.events_generated}")
        print(f"Packets Sent: {metrics.packets_sent}")
        print("=============================\n")

        await asyncio.sleep(1)


async def log_metrics():
    """
    Save metrics to CSV every second.
    """

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
            "packets_sent"
        ])

        while True:

            writer.writerow([
                time.time(),
                metrics.frames_sent,
                metrics.events_generated,
                metrics.packets_sent
            ])

            file.flush()

            await asyncio.sleep(1)


async def main():

    tasks = []

    # Create XR users
    for user_id in range(profile["users"]):

        tasks.append(
            asyncio.create_task(
                xr_user(user_id)
            )
        )

    # Metrics display
    tasks.append(
        asyncio.create_task(
            print_metrics()
        )
    )

    # CSV logger
    tasks.append(
        asyncio.create_task(
            log_metrics()
        )
    )

    await asyncio.gather(*tasks)


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nSimulation stopped.")