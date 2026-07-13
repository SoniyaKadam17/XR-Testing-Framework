import json
import asyncio
import csv
import time
from pathlib import Path
PROFILE_DIR = Path("profiles")


from src.tracking import TrackingSimulator
from src.user_behavior import UserBehavior
from src.video_stream import VideoStream
from src.metrics import Metrics
from src.packet_generator import PacketGenerator
from src.metrics_engine import MetricsEngine
from src.metrics_logger import MetricsLogger


# NEW COMPONENT 2 IMPORTS
from src.impairment_config import ImpairmentConfig
from src.impairment_engine import NetworkImpairmentEngine



# ==========================================
# Load XR Profile
# ==========================================

def load_profile(profile_name="high_load.json"):

    if not profile_name.endswith(".json"):
        profile_name += ".json"


    profile_path = PROFILE_DIR / profile_name


    with open(profile_path, "r") as file:
        return json.load(file)



# ==========================================
# Initialize Components
# ==========================================

tracking = TrackingSimulator()

behavior = UserBehavior()

video = VideoStream()

metrics = Metrics()

metrics_engine = MetricsEngine()

logger = MetricsLogger(metrics_engine)

packet_generator = PacketGenerator()



# ==========================================
# NETWORK IMPAIRMENT ENGINE
# ==========================================


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
        metrics_engine.record_packet_generated()

        processed_packet = network.process_packet(
            packet
        )



        # Packet dropped

        if processed_packet is None:
            metrics_engine.record_packet_dropped()


            continue



        # Check packets that finished network delay

        delivered_packets = (
            network.get_delivered_packets()
        )



        for pkt in delivered_packets:


            metrics.increment_packets()
            metrics_engine.record_packet_delivered()
            metrics.add_bytes(pkt["size"])
            metrics_engine.record_bytes(pkt["size"])
            metrics.add_latency(pkt["actual_latency_ms"])
            metrics_engine.record_latency(
                pkt["actual_latency_ms"]
            )


        # =================================================
        # COMPONENT 2 END
        # =================================================

        # =====================================
        # Component 3 - Queue Statistics
        # =====================================

        metrics_engine.record_queue_size(
            network.packet_queue.size()
        )

        metrics_engine.record_queue_wait(
            network.packet_queue.average_wait_time()
        )



        # -----------------------------
        # Existing Metrics
        # -----------------------------


        metrics.increment_frames()

        metrics_engine.record_frame()

        metrics.increment_events()

        metrics_engine.record_event()



        await asyncio.sleep(
            frame_interval
        )





# ==========================================
# Metrics Display
# ==========================================

async def print_metrics():


    while True:


        #metrics.print_metrics()
        logger.print_summary()


        print(
            network.get_statistics()
        )


        await asyncio.sleep(1)





# ==========================================
# CSV Logging
# ==========================================

async def log_metrics():

    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(exist_ok=True)

    results_csv = results_dir / "results.csv"

    with open(
        results_csv,
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
            logger.save_report(
                str(results_dir / "component3_metrics.csv"),
                str(results_dir / "component3_metrics.json")
            )


            await asyncio.sleep(1)





# ==========================================
# Main Traffic Scheduler
# ==========================================
import asyncio
import time


async def run_experiment(
    profile_name="high_load.json",
    latency_ms=50,
    jitter_ms=10,
    packet_loss_rate=0.02,
    bandwidth_mbps=50,
    duration_seconds=10
):

    global profile
    global network
    global metrics
    global metrics_engine
    global logger
    global packet_generator


    start_time = time.time()


    # -----------------------------------------
    # Reset all experiment-specific components
    # -----------------------------------------

    profile = load_profile(profile_name)
    profile["session_duration"] = duration_seconds

    metrics = Metrics()

    metrics_engine = MetricsEngine()

    logger = MetricsLogger(
        metrics_engine
    )

    packet_generator = PacketGenerator()



    # -----------------------------------------
    # Store experiment configuration
    # Required for Component 5/6
    # -----------------------------------------

    experiment_config = {

        "profile": profile_name,

        "latency_ms": latency_ms,

        "jitter_ms": jitter_ms,

        "packet_loss_rate": packet_loss_rate,

        "bandwidth_mbps": bandwidth_mbps

    }



    # -----------------------------------------
    # Create fresh Network Impairment Engine
    # -----------------------------------------

    network_config = ImpairmentConfig(

        latency_ms=latency_ms,

        jitter_ms=jitter_ms,

        packet_loss_rate=packet_loss_rate,

        bandwidth_mbps=bandwidth_mbps

    )


    network = NetworkImpairmentEngine(

        network_config

    )



    # -----------------------------------------
    # Run XR simulation
    # -----------------------------------------

    await main()



    # -----------------------------------------
    # Allow delayed packets to arrive
    # -----------------------------------------

    while network.packet_queue.size() > 0:

        await asyncio.sleep(0.1)



    # -----------------------------------------
    # Collect remaining delivered packets
    # -----------------------------------------

    remaining_packets = (
        network.get_delivered_packets()
    )


    for pkt in remaining_packets:


        metrics.increment_packets()


        metrics_engine.record_packet_delivered()



        metrics.add_bytes(
            pkt["size"]
        )


        metrics_engine.record_bytes(
            pkt["size"]
        )



        if "actual_latency_ms" in pkt:


            metrics.add_latency(
                pkt["actual_latency_ms"]
            )


            metrics_engine.record_latency(
                pkt["actual_latency_ms"]
            )



    # -----------------------------------------
    # Generate final metrics summary
    # -----------------------------------------

    summary = metrics_engine.get_summary()



    runtime = (
        time.time() - start_time
    )



    # -----------------------------------------
    # Return result
    # Used by:
    # Component 4 Controller
    # Component 5 Analysis
    # Component 6 Reporting
    # -----------------------------------------

    return {


        "configuration": experiment_config,


        "metrics": summary,


        "runtime_seconds": runtime

    }

    # -----------------------------------------
    # Finish metrics collection
    # -----------------------------------------

    metrics_engine.finish()

    # -----------------------------------------
    # Print summaries (keeps current behavior)
    # -----------------------------------------

    logger.print_summary()

    network_stats = network.get_statistics()

    print(network_stats)

    # -----------------------------------------
    # Return everything needed by
    # Experiment Controller
    # -----------------------------------------

    summary = metrics_engine.get_summary()

    return {
        "experiment_profile": profile["name"],
        "latency_ms": latency_ms,
        "jitter_ms": jitter_ms,
        "packet_loss_percent": packet_loss_rate * 100,
        "bandwidth_mbps": bandwidth_mbps,
        **network_stats,
        **summary
    }

async def main():

    print("\n========== XR WORKLOAD ==========")

    print(f"Profile: {profile['name']}")
    print(f"Users: {profile['users']}")
    print(f"FPS: {profile['fps']}")
    print(f"Packet Size: {profile['packet_size']} bytes")

    print("=================================\n")

    # XR user tasks
    user_tasks = [

        asyncio.create_task(
            xr_user(user_id)
        )

        for user_id in range(profile["users"])

    ]

    # Background tasks
    metrics_task = asyncio.create_task(
        print_metrics()
    )

    logging_task = asyncio.create_task(
        log_metrics()
    )

    # Wait only for XR users to finish
    await asyncio.gather(*user_tasks)
    # Allow remaining delayed packets to arrive
    await asyncio.sleep(1)

    remaining_packets = network.get_delivered_packets()

    for pkt in remaining_packets:
        metrics.increment_packets()
        metrics_engine.record_packet_delivered()
        metrics.add_bytes(pkt["size"])
        metrics_engine.record_bytes(pkt["size"])
        metrics.add_latency(pkt["actual_latency_ms"])
        metrics_engine.record_latency(pkt["actual_latency_ms"])

    # Stop background tasks
    metrics_task.cancel()
    logging_task.cancel()

    try:
        await metrics_task
    except asyncio.CancelledError:
        pass

    try:
        await logging_task
    except asyncio.CancelledError:
        pass




# ==========================================
# Start
# ==========================================

if __name__ == "__main__":

    try:
        asyncio.run(
            run_experiment()
        )

    except KeyboardInterrupt:
        print("\nSimulation stopped.")