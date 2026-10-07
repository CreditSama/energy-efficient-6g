import numpy as np


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
    )