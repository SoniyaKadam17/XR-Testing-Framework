import pandas as pd
import matplotlib.pyplot as plt
import os



RESULT_FILE = "../results/results.csv"



if not os.path.exists(RESULT_FILE):

    print("results.csv not found")

    exit()



df = pd.read_csv(RESULT_FILE)



# -----------------------------
# Bandwidth Graph
# -----------------------------

def bandwidth_graph():

    plt.figure(figsize=(10,5))

    plt.plot(
        df["timestamp"],
        df["bandwidth_mbps"]
    )

    plt.title(
        "XR Bandwidth Usage"
    )

    plt.xlabel(
        "Time"
    )

    plt.ylabel(
        "Mbps"
    )

    plt.grid(True)

    plt.savefig(
        "../results/bandwidth.png"
    )

    plt.close()



# -----------------------------
# Frames Graph
# -----------------------------

def frames_graph():

    plt.figure(figsize=(10,5))


    plt.plot(
        df["timestamp"],
        df["frames_sent"]
    )


    plt.title(
        "XR Frames Generated"
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Frames"
    )


    plt.grid(True)


    plt.savefig(
        "../results/frames.png"
    )


    plt.close()




# -----------------------------
# Packets Graph
# -----------------------------

def packets_graph():

    plt.figure(figsize=(10,5))


    plt.plot(

        df["timestamp"],

        df["packets_sent"]

    )


    plt.title(
        "XR Packets Sent"
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Packets"
    )


    plt.grid(True)


    plt.savefig(
        "../results/packets.png"
    )


    plt.close()




# -----------------------------
# Latency Graph
# -----------------------------

def latency_graph():

    plt.figure(figsize=(10,5))


    plt.plot(

        df["timestamp"],

        df["avg_latency_ms"],

        label="Average"

    )


    plt.plot(

        df["timestamp"],

        df["min_latency_ms"],

        label="Minimum"

    )


    plt.plot(

        df["timestamp"],

        df["max_latency_ms"],

        label="Maximum"

    )


    plt.title(
        "XR Network Latency"
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Latency (ms)"
    )


    plt.legend()


    plt.grid(True)


    plt.savefig(
        "../results/latency.png"
    )


    plt.close()




# -----------------------------
# Summary Graph
# -----------------------------

def summary_graph():


    metrics = [

        "Bandwidth Mbps",

        "Avg Latency ms",

        "Total Frames",

        "Total Packets"

    ]


    values = [

        df["bandwidth_mbps"].mean(),

        df["avg_latency_ms"].mean(),

        df["frames_sent"].iloc[-1],

        df["packets_sent"].iloc[-1]

    ]



    plt.figure(figsize=(8,5))


    plt.bar(

        metrics,

        values

    )


    plt.title(
        "XR Performance Summary"
    )


    plt.xticks(
        rotation=30
    )


    plt.grid(True)



    plt.savefig(

        "../results/summary.png"

    )


    plt.close()




# -----------------------------
# Terminal Summary
# -----------------------------

print("\n========== XR PERFORMANCE SUMMARY ==========")


print(
    "Total Frames:",
    df["frames_sent"].iloc[-1]
)


print(
    "Total Packets:",
    df["packets_sent"].iloc[-1]
)


print(
    "Total Data:",
    round(
        df["bytes_sent"].iloc[-1]/1024/1024,
        2
    ),
    "MB"
)


print(
    "Average Bandwidth:",
    round(
        df["bandwidth_mbps"].mean(),
        2
    ),
    "Mbps"
)


print(
    "Average Latency:",
    round(
        df["avg_latency_ms"].mean(),
        2
    ),
    "ms"
)


print(
    "Peak Latency:",
    round(
        df["max_latency_ms"].max(),
        2
    ),
    "ms"
)


print(
    "============================================"
)



bandwidth_graph()

frames_graph()

packets_graph()

latency_graph()

summary_graph()



print("\nDashboard generated successfully")

print(
"""
Generated files:

../results/bandwidth.png
../results/frames.png
../results/packets.png
../results/latency.png
../results/summary.png

"""
)