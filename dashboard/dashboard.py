import pandas as pd
import matplotlib.pyplot as plt
import os


# ------------------------------------
# File Location
# ------------------------------------

CSV_FILE = "../results/results.csv"


# ------------------------------------
# Load CSV Data
# ------------------------------------

def load_data():

    if not os.path.exists(CSV_FILE):

        print("result.csv not found")

        exit()


    data = pd.read_csv(
        CSV_FILE
    )

    return data



# ------------------------------------
# Convert Timestamp
# ------------------------------------

def process_time(data):

    data["time"] = (
        data["timestamp"]
        -
        data["timestamp"].iloc[0]
    )

    return data



# ------------------------------------
# Bandwidth Graph
# ------------------------------------

def plot_bandwidth(data):

    plt.figure(figsize=(8,5))


    plt.plot(
        data["time"],
        data["bandwidth_mbps"]
    )


    plt.xlabel(
        "Time (seconds)"
    )


    plt.ylabel(
        "Bandwidth (Mbps)"
    )


    plt.title(
        "XR Workload Bandwidth Usage"
    )


    plt.grid()


    plt.savefig(
        "../results/bandwidth.png"
    )


    plt.close()



# ------------------------------------
# Packet Graph
# ------------------------------------

def plot_packets(data):

    plt.figure(figsize=(8,5))


    plt.plot(
        data["time"],
        data["packets_sent"]
    )


    plt.xlabel(
        "Time (seconds)"
    )


    plt.ylabel(
        "Packets Sent"
    )


    plt.title(
        "XR Packet Transmission Rate"
    )


    plt.grid()


    plt.savefig(
        "../results/packets.png"
    )


    plt.close()



# ------------------------------------
# Frames Graph
# ------------------------------------

def plot_frames(data):

    plt.figure(figsize=(8,5))


    plt.plot(
        data["time"],
        data["frames_sent"]
    )


    plt.xlabel(
        "Time (seconds)"
    )


    plt.ylabel(
        "Frames"
    )


    plt.title(
        "XR Frame Generation"
    )


    plt.grid()


    plt.savefig(
        "../results/frames.png"
    )


    plt.close()



# ------------------------------------
# Generate Summary
# ------------------------------------

def generate_summary(data):


    total_frames = (
        data["frames_sent"]
        .iloc[-1]
    )


    total_packets = (
        data["packets_sent"]
        .iloc[-1]
    )


    total_bytes = (
        data["bytes_sent"]
        .iloc[-1]
    )


    average_bandwidth = (
        data["bandwidth_mbps"]
        .mean()
    )


    peak_bandwidth = (
        data["bandwidth_mbps"]
        .max()
    )


    print("\n========== XR PERFORMANCE SUMMARY ==========")


    print(
        f"Total Frames: {total_frames}"
    )


    print(
        f"Total Packets: {total_packets}"
    )


    print(
        f"Total Data: {total_bytes / (1024*1024):.2f} MB"
    )


    print(
        f"Average Bandwidth: {average_bandwidth:.2f} Mbps"
    )


    print(
        f"Peak Bandwidth: {peak_bandwidth:.2f} Mbps"
    )


    print(
        "============================================"
    )



# ------------------------------------
# Main
# ------------------------------------

def main():


    data = load_data()


    data = process_time(
        data
    )


    plot_bandwidth(
        data
    )


    plot_packets(
        data
    )


    plot_frames(
        data
    )


    generate_summary(
        data
    )


    print(
        "\nDashboard generated successfully"
    )


    print(
        "Generated files:"
    )

    print(
        "../results/bandwidth.png"
    )

    print(
        "../results/packets.png"
    )

    print(
        "../results/frames.png"
    )



if __name__ == "__main__":

    main()