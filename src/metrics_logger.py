"""
Metrics Logger

Responsible for saving and displaying metrics collected
by the Metrics Collection Engine.

Outputs:
- Console Summary
- CSV Log
- JSON Report
"""

import csv
import json
import os
import time


class MetricsLogger:

    def __init__(self, metrics_engine):

        self.metrics = metrics_engine

    # ==========================================
    # Console Output
    # ==========================================

    def print_summary(self):

        summary = self.metrics.summary()

        print("\n========== METRICS COLLECTION ENGINE ==========\n")

        print(f"Frames Sent          : {summary['Frames Sent']}")
        print(f"Events Generated     : {summary['Events Generated']}")

        print()

        print(f"Total Packets        : {summary['Total Packets']}")
        print(f"Delivered Packets    : {summary['Delivered Packets']}")
        print(f"Dropped Packets      : {summary['Dropped Packets']}")

        print()

        print(f"Packet Loss          : {summary['Packet Loss %']} %")
        print(f"Delivery Ratio       : {summary['Delivery Ratio %']} %")

        print()

        print(f"Bytes Sent           : {summary['Bytes Sent']}")

        print()

        print(f"Average Latency      : {summary['Average Latency']} ms")
        print(f"Minimum Latency      : {summary['Minimum Latency']} ms")
        print(f"Maximum Latency      : {summary['Maximum Latency']} ms")
        print(f"Average Jitter       : {summary['Average Jitter']} ms")

        print()

        print(f"Average Queue Size   : {summary['Average Queue Size']}")
        print(f"Maximum Queue Size   : {summary['Maximum Queue Size']}")
        print(f"Average Queue Wait   : {summary['Average Queue Wait']} ms")

        print()

        print(f"Throughput           : {summary['Throughput']} Mbps")
        print(f"Runtime              : {summary['Runtime']} seconds")

        print("\n===============================================\n")

    # ==========================================
    # CSV Logging
    # ==========================================

    def write_csv(self, filename):

        summary = self.metrics.summary()

        file_exists = os.path.isfile(filename)

        with open(filename, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "timestamp",

                    "frames_sent",
                    "events_generated",

                    "total_packets",
                    "delivered_packets",
                    "dropped_packets",

                    "packet_loss_percent",
                    "delivery_ratio",

                    "bytes_sent",

                    "average_latency_ms",
                    "minimum_latency_ms",
                    "maximum_latency_ms",

                    "average_jitter_ms",

                    "average_queue_size",
                    "maximum_queue_size",
                    "average_queue_wait_ms",

                    "throughput_mbps",

                    "runtime_seconds"
                ])

            writer.writerow([

                time.time(),

                summary["Frames Sent"],
                summary["Events Generated"],

                summary["Total Packets"],
                summary["Delivered Packets"],
                summary["Dropped Packets"],

                summary["Packet Loss %"],
                summary["Delivery Ratio %"],

                summary["Bytes Sent"],

                summary["Average Latency"],
                summary["Minimum Latency"],
                summary["Maximum Latency"],

                summary["Average Jitter"],

                summary["Average Queue Size"],
                summary["Maximum Queue Size"],
                summary["Average Queue Wait"],

                summary["Throughput"],

                summary["Runtime"]
            ])

    # ==========================================
    # JSON Logging
    # ==========================================

    def write_json(self, filename):

        summary = self.metrics.summary()

        with open(filename, "w") as file:

            json.dump(
                summary,
                file,
                indent=4
            )

    # ==========================================
    # Complete Report
    # ==========================================

    def save_report(self,
                    csv_file,
                    json_file):

        self.write_csv(csv_file)

        self.write_json(json_file)

    # ==========================================
    # Final Experiment Report
    # ==========================================

    def print_final_report(self):

        self.metrics.finish()

        self.print_summary()