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

            self.df["Latency"],

            self.df["Average Latency"],

            "Configured Latency (ms)",

            "Measured Latency (ms)",

            "latency.png"

        )

        self.save_plot(

            self.df["Latency"],

            self.df["Throughput"],

            "Configured Latency (ms)",

            "Throughput (Mbps)",

            "throughput.png"

        )

        self.save_plot(

            self.df["Latency"],

            self.df["Average Queue Size"],

            "Configured Latency (ms)",

            "Queue Size",

            "queue_size.png"

        )

        self.save_plot(

            self.df["Latency"],

            self.df["Average Queue Wait"],

            "Configured Latency (ms)",

            "Queue Wait (ms)",

            "queue_wait.png"

        )

        self.save_plot(

            self.df["Latency"],

            self.df["Average Jitter"],

            "Configured Latency (ms)",

            "Average Jitter (ms)",

            "jitter.png"

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

            "queue_size.png",

            "queue_wait.png",

            "jitter.png"

        ]

        for img in images:

            story.append(

                Paragraph(

                    img.replace(".png", ""),

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