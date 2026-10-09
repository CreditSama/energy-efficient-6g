
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load simulation results
data = pd.read_csv("results/network_results.csv")

# Create results folder if it doesn't exist
os.makedirs("results", exist_ok=True)

# Plot distance vs received power
plt.figure(figsize=(9, 5))

plt.scatter(
    data["Distance_m"],
    data["Received_Power_mW"],
    color="blue",
    s=70,
    edgecolors="black"
)

plt.xlabel("Distance from Base Station (m)")
plt.ylabel("Received Power (mW)")
plt.title("Distance vs Received Power in a 6G Network")
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("results/distance_vs_received_power.png", dpi=300)

print("Graph saved to results/distance_vs_received_power.png")

plt.show()

# Graph 2: Throughput per user
plt.figure(figsize=(9, 5))

plt.bar(data["User"], data["Throughput_bps"] / 1e6)

plt.xlabel("User ID")
plt.ylabel("Throughput (Mbps)")
plt.title("Throughput of Each User")
plt.xticks(data["User"])
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("results/user_throughput.png", dpi=300)

print("Throughput graph saved to results/user_throughput.png")
plt.show()

# Graph 3: Energy efficiency per user
# Approximate each user's share of total transmit power.
total_power_w = 1.0  # 10 users × 100 mW each
user_power_w = total_power_w / len(data)

data["Energy_Efficiency_bits_per_J"] = (
    data["Throughput_bps"] / user_power_w
)

plt.figure(figsize=(9, 5))

plt.bar(
    data["User"],
    data["Energy_Efficiency_bits_per_J"] / 1e6
)

plt.xlabel("User ID")
plt.ylabel("Energy Efficiency (Mbits/J)")
plt.title("Energy Efficiency of Each User")
plt.xticks(data["User"])
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("results/user_energy_efficiency.png", dpi=300)

print("Energy-efficiency graph saved to results/user_energy_efficiency.png")
plt.show()

# Graph 4: Fixed vs dynamic allocation
comparison = pd.read_csv("results/comparison_results.csv")

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

axes[0].bar(comparison["Method"], comparison["Power_W"])
axes[0].set_title("Total Transmit Power")
axes[0].set_ylabel("Power (W)")

axes[1].bar(comparison["Method"], comparison["Throughput_Mbps"])
axes[1].set_title("Total Throughput")
axes[1].set_ylabel("Throughput (Mbps)")

axes[2].bar(
    comparison["Method"],
    comparison["Efficiency_Mbits_per_J"]
)
axes[2].set_title("Energy Efficiency")
axes[2].set_ylabel("Mbits/J")

for ax in axes:
    ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.suptitle("Fixed vs Dynamic Power Allocation")
plt.tight_layout()
plt.savefig("results/fixed_vs_dynamic_comparison.png", dpi=300)
plt.show()

print("Comparison graph saved.")

# Graph 5: QoS comparison
plt.figure(figsize=(7, 5))

plt.bar(
    comparison["Method"],
    comparison["QoS_Users_Met"]
)

plt.axhline(
    y=10,
    linestyle="--",
    label="All 10 users"
)

plt.xlabel("Power Allocation Method")
plt.ylabel("Users Meeting QoS Target")
plt.title("QoS Satisfaction: Fixed vs Dynamic Allocation")
plt.ylim(0, 11)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/qos_comparison.png", dpi=300)
plt.show()

print("QoS graph saved to results/qos_comparison.png")