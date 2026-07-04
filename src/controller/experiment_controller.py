import json
from pathlib import Path
from itertools import product


class ExperimentController:
    """
    Controls the execution of XR network experiments.
    """

    def __init__(self):
        # Project root directory
        self.project_root = Path(__file__).resolve().parents[2]

        # Configuration file
        self.config_path = self.project_root / "config" / "experiments.json"

        self.config = {}
        self.experiments = []

    def load_configuration(self):
        """
        Load experiment configuration from JSON.
        """

        print(f"Loading configuration from:\n{self.config_path}\n")

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found:\n{self.config_path}"
            )

        with open(self.config_path, "r") as file:
            self.config = json.load(file)

        print("✓ Configuration loaded successfully.")

    def validate_configuration(self):
        """
        Validate required configuration sections.
        """

        required_sections = [
            "experiment",
            "xr_workload",
            "network_conditions",
            "metrics",
            "logging"
        ]

        for section in required_sections:
            if section not in self.config:
                raise ValueError(
                    f"Missing configuration section: {section}"
                )

        print("✓ Configuration validated.")

    def generate_experiments(self):
        """
        Generate all experiment combinations.
        """

        network = self.config["network_conditions"]

        latencies = network["latency_ms"]
        losses = network["packet_loss_percent"]
        jitters = network["jitter_ms"]
        bandwidths = network["bandwidth_mbps"]

        experiment_id = 1

        for latency, loss, jitter, bandwidth in product(
            latencies,
            losses,
            jitters,
            bandwidths
        ):

            self.experiments.append(
                {
                    "experiment_id": experiment_id,
                    "latency_ms": latency,
                    "packet_loss_percent": loss,
                    "jitter_ms": jitter,
                    "bandwidth_mbps": bandwidth,
                }
            )

            experiment_id += 1

        print(f"✓ Generated {len(self.experiments)} experiments.")

    def show_experiment_plan(self):
        """
        Display experiment plan.
        """

        print("\nExperiment Plan")
        print("-" * 80)

        for experiment in self.experiments:

            print(
                f"Experiment {experiment['experiment_id']:3d} | "
                f"Latency={experiment['latency_ms']:3d} ms | "
                f"Loss={experiment['packet_loss_percent']:2d}% | "
                f"Jitter={experiment['jitter_ms']:2d} ms | "
                f"Bandwidth={experiment['bandwidth_mbps']:3d} Mbps"
            )

        print("-" * 80)
        print(f"Total Experiments: {len(self.experiments)}")


def main():

    controller = ExperimentController()

    controller.load_configuration()

    controller.validate_configuration()

    controller.generate_experiments()

    controller.show_experiment_plan()


if __name__ == "__main__":
    main()