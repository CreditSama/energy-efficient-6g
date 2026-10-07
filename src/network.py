import numpy as np
from channel import (
    calculate_path_loss,
    calculate_channel_gain,
    calculate_received_power,
    calculate_sinr,
    calculate_throughput
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
    )