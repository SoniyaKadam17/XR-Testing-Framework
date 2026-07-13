"""
Experiment Controller
Component 4

Responsible for:
- Loading experiment configurations
- Generating experiment scenarios
- Executing XR simulations
- Collecting metrics
- Saving results for:
    Component 5: Data Analysis
    Component 6: Reporting Engine
"""

import os
import json
import csv
import asyncio
from datetime import datetime


# Existing project imports
from src.main import run_experiment
from src.metrics_engine import MetricsEngine


CONFIG_PATH = "config/experiments.json"

RESULT_DIR = "results"

RESULT_JSON = os.path.join(
    RESULT_DIR,
    "experiment_results.json"
)

RESULT_CSV = os.path.join(
    RESULT_DIR,
    "experiment_results.csv"
)



class ExperimentController:


    def __init__(self):

        self.experiments = []

        self.results = []

        os.makedirs(
            RESULT_DIR,
            exist_ok=True
        )


    # ---------------------------------
    # Load experiment configuration
    # ---------------------------------

    def load_config(self):

        print("\nLoading experiment configuration...")

        with open(CONFIG_PATH,"r") as file:

            config=json.load(file)


        self.generate_experiments(config)


        print(
            f"Generated {len(self.experiments)} experiments"
        )



    # ---------------------------------
    # Generate experiment combinations
    # ---------------------------------

    def generate_experiments(self, config):


        profile = config["xr_workload"]["profile"]


        latencies = config["network_conditions"]["latency_ms"]

        losses = config["network_conditions"]["packet_loss_percent"]

        jitters = config["network_conditions"]["jitter_ms"]

        bandwidths = config["network_conditions"]["bandwidth_mbps"]


        experiment_id = 1


        for latency in latencies:

            for loss in losses:

                for jitter in jitters:

                    for bandwidth in bandwidths:


                        experiment = {

                            "experiment_id": experiment_id,

                            "profile": profile,

                            "latency_ms": latency,

                            "packet_loss_rate": loss / 100,

                            "packet_loss_percent": loss,

                            "jitter_ms": jitter,

                            "bandwidth_mbps": bandwidth

                        }


                        self.experiments.append(
                            experiment
                        )


                        experiment_id += 1


    # ---------------------------------
    # Execute experiments
    # ---------------------------------

    async def run_all(self):


        print(
            "\n========== EXPERIMENT EXECUTION =========="
        )


        for experiment in self.experiments[:3]:


            print(
                f"\nRunning Experiment "
                f"{experiment['experiment_id']}"
            )


            result = await self.run_single(
                experiment
            )


            self.results.append(result)



        self.save_results()



    # ---------------------------------
    # Run single experiment
    # ---------------------------------

    async def run_single(
            self,
            experiment
    ):


        start_time=datetime.now()


        metrics = await run_experiment(

            profile_name=experiment["profile"],
            latency_ms=experiment["latency_ms"],
            jitter_ms=experiment["jitter_ms"],
            packet_loss_rate=experiment["packet_loss_rate"],
            bandwidth_mbps=experiment["bandwidth_mbps"],
            duration_seconds=10

        )


        end_time=datetime.now()


        result={

            "experiment_id":
                experiment["experiment_id"],

            "configuration":
                experiment,


            "metrics":
                metrics,


            "runtime_seconds":
                (
                    end_time-start_time
                ).total_seconds(),


            "timestamp":
                str(datetime.now())

        }


        return result



    # ---------------------------------
    # Save results
    # Needed by Component 5/6
    # ---------------------------------

    def save_results(self):


        print(
            "\nSaving experiment results..."
        )


        # JSON

        with open(
            RESULT_JSON,
            "w"
        ) as file:

            json.dump(
                self.results,
                file,
                indent=4
            )



        # CSV

        with open(
            RESULT_CSV,
            "w",
            newline=""
        ) as file:


            writer=csv.writer(file)


            writer.writerow(
                [

                "Experiment ID",
                "Profile",
                "Latency(ms)",
                "Loss(%)",
                "Jitter(ms)",
                "Bandwidth(Mbps)",
                "Packets",
                "Dropped",
                "Packet Loss %",
                "Average Latency",
                "Throughput"

                ]
            )



            for r in self.results:


                cfg=r["configuration"]

                m = r["metrics"]["metrics"]


                writer.writerow(
                    [

                    r["experiment_id"],

                    cfg["profile"],

                    cfg["latency_ms"],

                    cfg["packet_loss_rate"],

                    cfg["jitter_ms"],

                    cfg["bandwidth_mbps"],

                    m.get(
                        "Total Packets"
                    ),

                    m.get(
                        "Dropped Packets"
                    ),

                    m.get(
                        "Packet Loss %"
                    ),

                    m.get(
                        "Average Latency"
                    ),

                    m.get(
                        "Throughput"
                    )

                    ]
                )



        print(
            "Results saved:"
        )

        print(
            RESULT_JSON
        )

        print(
            RESULT_CSV
        )





async def main():


    controller = ExperimentController()


    controller.load_config()


    await controller.run_all()



if __name__=="__main__":


    asyncio.run(main())