import os
import numpy as np
from channel import (
    calculate_path_loss,
    calculate_channel_gain,
    calculate_received_power,
    calculate_sinr,
    calculate_throughput
)

from optimization import allocate_dynamic_power
import pandas as pd
from energy import (
    calculate_total_power,
    calculate_energy_consumption,
    calculate_energy_efficiency
)


# -----------------------------
# Network Configuration
# -----------------------------

AREA_SIZE = 500  # Network area in meters
NUM_USERS = 10   # Number of users


# -----------------------------
# Base Station
# -----------------------------

base_station = np.array([AREA_SIZE / 2, AREA_SIZE / 2])


# -----------------------------
# Generate User Positions
# -----------------------------

np.random.seed(42)

user_positions = np.random.uniform(
    0,
    AREA_SIZE,
    size=(NUM_USERS, 2)
)


# -----------------------------
# Calculate Distance
# -----------------------------

distances = np.linalg.norm(
    user_positions - base_station,
    axis=1
)
# -----------------------------
# Calculate Path Loss
# -----------------------------

path_loss = calculate_path_loss(distances)
channel_gain = calculate_channel_gain(path_loss)
# -----------------------------
# Calculate Received Power
# -----------------------------

TRANSMIT_POWER = 100  # mW

received_power = calculate_received_power(
    TRANSMIT_POWER,
    channel_gain
)
# -----------------------------
# Calculate SINR
# -----------------------------

NOISE_POWER = 1e-9  # mW

sinr = calculate_sinr(
    received_power,
    NOISE_POWER
)
# -----------------------------
# Calculate Throughput
# -----------------------------

BANDWIDTH = 100e6  # 100 MHz

throughput = calculate_throughput(
    sinr,
    BANDWIDTH
)
# -----------------------------
# Energy Metrics
# -----------------------------

transmit_powers = np.full(NUM_USERS, TRANSMIT_POWER)

SIMULATION_TIME = 1.0  # seconds
CIRCUIT_POWER = 0.0    # W; initially excluded

total_power_w = calculate_total_power(
    transmit_powers,
    CIRCUIT_POWER
)

total_throughput_bps = np.sum(throughput)

energy_joules = calculate_energy_consumption(
    total_power_w,
    SIMULATION_TIME
)

energy_efficiency = calculate_energy_efficiency(
    total_throughput_bps,
    total_power_w
)

# Dynamic power allocation
TARGET_RATE_BPS = 10e6  # Target: 10 Mbps per user

dynamic_power_mw = allocate_dynamic_power(
    channel_gain=channel_gain,
    noise_power=NOISE_POWER,
    bandwidth=BANDWIDTH,
    target_rate_bps=TARGET_RATE_BPS,
    min_power_mw=1.0,
    max_power_mw=TRANSMIT_POWER
)

# Calculate received power and SNR using dynamic allocation
dynamic_received_power = dynamic_power_mw * channel_gain
dynamic_snr = dynamic_received_power / NOISE_POWER

# Calculate throughput under dynamic allocation
dynamic_throughput = BANDWIDTH * np.log2(1 + dynamic_snr)

# Calculate total power and energy
dynamic_total_power_w = np.sum(dynamic_power_mw) / 1000
dynamic_energy_j = dynamic_total_power_w * SIMULATION_TIME

# Calculate energy efficiency
dynamic_total_throughput = np.sum(dynamic_throughput)

dynamic_efficiency = (
    dynamic_total_throughput / dynamic_total_power_w
    if dynamic_total_power_w > 0
    else 0.0
)
results = pd.DataFrame({
    "User": np.arange(1, NUM_USERS + 1),
    "Distance_m": distances,
    "Path_Loss_dB": path_loss,
    "Channel_Gain": channel_gain,
    "Received_Power_mW": received_power,
    "SNR": sinr,
    "Throughput_bps": throughput
})
os.makedirs("results", exist_ok=True)
results.to_csv("results/network_results.csv", index=False)

print("\nResults saved to results/network_results.csv")

# -----------------------------
# Display Results
# -----------------------------

print("6G Energy-Efficient Network Simulation")
print("---------------------------------------")

print(f"Network area: {AREA_SIZE} x {AREA_SIZE} meters")
print(f"Number of users: {NUM_USERS}")

print("\nBase Station Position:")
print(base_station)

print("\nUser Information:")

for i in range(NUM_USERS):
    print(
        f"User {i + 1}: "
        f"Position = {user_positions[i]}, "
        f"Distance = {distances[i]:.2f} m"
        f"Path Loss = {path_loss[i]:.2f} dB"
        f"Channel Gain = {channel_gain[i]:.2e}"
        f"Received Power = {received_power[i]:.2e} mW"
        f"SINR = {sinr[i]:.2f}"
        f"Throughput = {throughput[i] / 1e6:.2f} Mbps"
        f"Energy efficiency: {energy_efficiency:.2e} bits/J"
    )
    
print("\n========== FIXED vs DYNAMIC POWER ==========")

print("\nFixed Power Allocation:")
print(f"Total Power: {total_power_w:.4f} W")
print(f"Total Throughput: {total_throughput_bps / 1e6:.2f} Mbps")
print(f"Energy Efficiency: {energy_efficiency / 1e6:.2f} Mbits/J")

print("\nDynamic Power Allocation:")
print(f"Total Power: {dynamic_total_power_w:.4f} W")
print(f"Total Throughput: {dynamic_total_throughput / 1e6:.2f} Mbps")
print(f"Energy Efficiency: {dynamic_efficiency / 1e6:.2f} Mbits/J")

if total_power_w > 0:
    energy_saving_percent = (
        (total_power_w - dynamic_total_power_w)
        / total_power_w
    ) * 100
    print(f"\nEnergy/Power Reduction: {energy_saving_percent:.2f}%")
    
# QoS analysis: minimum target rate per user
fixed_qos_met = throughput >= TARGET_RATE_BPS

# Allow a tiny tolerance for floating-point rounding
dynamic_qos_met = (
    dynamic_throughput >= TARGET_RATE_BPS * (1 - 1e-9)
)
print("\n========== QoS ANALYSIS ==========")
print(f"Target rate per user: {TARGET_RATE_BPS / 1e6:.1f} Mbps")

print(
    f"Fixed allocation: {np.sum(fixed_qos_met)} "
    f"/ {NUM_USERS} users meet the target"
)

print(
    f"Dynamic allocation: {np.sum(dynamic_qos_met)} "
    f"/ {NUM_USERS} users meet the target"
)

print("\nPer-user QoS:")
for i in range(NUM_USERS):
    print(
        f"User {i + 1}: "
        f"Fixed = {throughput[i] / 1e6:.2f} Mbps, "
        f"Dynamic = {dynamic_throughput[i] / 1e6:.2f} Mbps"
    )
    
comparison = pd.DataFrame({
    "Method": ["Fixed", "Dynamic"],
    "Power_W": [total_power_w, dynamic_total_power_w],
    "Throughput_Mbps": [
        total_throughput_bps / 1e6,
        dynamic_total_throughput / 1e6
    ],
    "Efficiency_Mbits_per_J": [
        energy_efficiency / 1e6,
        dynamic_efficiency / 1e6
    ],
    "QoS_Users_Met": [
        int(np.sum(throughput >= TARGET_RATE_BPS)),
        int(np.sum(dynamic_throughput >= TARGET_RATE_BPS * (1 - 1e-9)))
    ]
})

os.makedirs("results", exist_ok=True)
comparison.to_csv("results/comparison_results.csv", index=False)

print("\nComparison results saved.")

# Detailed optimization validation
print("\n========== OPTIMIZATION VALIDATION ==========")

print(f"Power limit per user: {TRANSMIT_POWER:.1f} mW")
print(f"Minimum target rate: {TARGET_RATE_BPS / 1e6:.1f} Mbps")

print("\nUser | Allocated Power (mW) | Throughput (Mbps) | QoS")
print("-" * 60)

for i in range(NUM_USERS):
    qos_status = (
        "PASS"
        if dynamic_throughput[i] >= TARGET_RATE_BPS * (1 - 1e-9)
        else "FAIL"
    )

    print(
        f"{i + 1:4d} | "
        f"{dynamic_power_mw[i]:20.4f} | "
        f"{dynamic_throughput[i] / 1e6:17.2f} | "
        f"{qos_status}"
    )

print("-" * 60)
print(f"Users meeting QoS: {np.sum(dynamic_qos_met)}/{NUM_USERS}")
print(f"Total dynamic power: {dynamic_total_power_w:.4f} W")