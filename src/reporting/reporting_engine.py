from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer
)


class ReportingEngine:

    def __init__(self):

        self.results_dir = (
            Path(__file__).resolve().parents[2]
            / "results"
        )

        self.report_dir = (
            self.results_dir
            / "report"
        )

        self.report_dir.mkdir(
            exist_ok=True
        )

        self.summary_csv = (
            self.results_dir
            / "analysis_summary.csv"
        )

        self.statistics_json = (
            self.results_dir
            / "statistics.json"
        )

        self.df = None

        self.statistics = None

    ####################################################

    def load_files(self):

        self.df = pd.read_csv(
            self.summary_csv
        )

        with open(
            self.statistics_json
        ) as f:

            self.statistics = json.load(f)

    ####################################################

    def save_plot(
        self,
        x,
        y,
        xlabel,
        ylabel,
        filename
    ):

        plt.figure(figsize=(8, 5))

        plt.plot(
            x,
            y,
            marker="o"
        )

        plt.xlabel(xlabel)

        plt.ylabel(ylabel)

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            self.report_dir / filename
        )

        plt.close()

    ####################################################

    def generate_graphs(self):

        self.save_plot(
            self.df["Latency(ms)"],
            self.df["Average Latency"],
            "Configured Latency (ms)",
            "Measured Latency (ms)",
            "latency.png"
        )

        self.save_plot(
            self.df["Latency(ms)"],
            self.df["Throughput"],
            "Configured Latency (ms)",
            "Throughput (Mbps)",
            "throughput.png"
        )

        self.save_plot(
            self.df["Latency(ms)"],
            self.df["Packet Loss %"],
            "Configured Latency (ms)",
            "Packet Loss (%)",
            "packet_loss.png"
        )

        self.save_plot(
            self.df["Bandwidth(Mbps)"],
            self.df["Throughput"],
            "Bandwidth (Mbps)",
            "Throughput (Mbps)",
            "bandwidth.png"
        )

        self.save_plot(
            self.df["Experiment ID"] if "Experiment ID" in self.df.columns else range(1, len(self.df)+1),
            self.df["Throughput"],
            "Experiment",
            "Throughput (Mbps)",
            "comparison.png"
        )

    ####################################################

    def build_pdf(self):

        pdf = SimpleDocTemplate(

            str(
                self.report_dir
                / "final_report.pdf"
            )

        )

        styles = getSampleStyleSheet()

        story = []

        story.append(

            Paragraph(

                "XR Network Testing Report",

                styles["Heading1"]

            )

        )

        story.append(
            Spacer(1, 20)
        )

        story.append(

            Paragraph(

                "Overall Statistics",

                styles["Heading2"]

            )

        )

        story.append(
            Spacer(1, 10)
        )

        for key, value in self.statistics.items():

            story.append(

                Paragraph(

                    f"<b>{key}</b>: {value}",

                    styles["BodyText"]

                )

            )

        story.append(
            Spacer(1, 20)
        )

        images = [

            "latency.png",

            "throughput.png",

            "packet_loss.png",

            "bandwidth.png",

            "comparison.png"

        ]

        for img in images:


                titles = {
                    "latency.png": "Latency Analysis",
                    "throughput.png": "Throughput Analysis",
                    "packet_loss.png": "Packet Loss Analysis",
                    "bandwidth.png": "Bandwidth vs Throughput",
                    "comparison.png": "Experiment Comparison"
                }

                story.append(
                    Paragraph(
                        titles[img],
                        styles["Heading2"]
                    )
                )

                story.append(
                    Spacer(1, 10)
                )

                story.append(

                    Image(

                        str(
                            self.report_dir
                            / img
                        ),

                        width=420,

                        height=260

                    )

                )

                story.append(
                    Spacer(1, 20)
                )

        pdf.build(story)

    ####################################################

    def run(self):

        self.load_files()

        self.generate_graphs()

        self.build_pdf()

        print()

        print("========== REPORTING ENGINE ==========")

        print("Graphs generated.")

        print("PDF report created.")

        print(self.report_dir)

        print("=======================================")


###########################################################


def main():

    ReportingEngine().run()


###########################################################


if __name__ == "__main__":

    main()