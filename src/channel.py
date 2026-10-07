import numpy as np


# -----------------------------
# Path Loss Model
# -----------------------------

def calculate_path_loss(
    distances,
    reference_distance=1.0,
    reference_path_loss=40.0,
    path_loss_exponent=3.0
):
    """
    Calculate path loss using the log-distance path loss model.
    """

    distances = np.maximum(distances, reference_distance)

    path_loss = (
        reference_path_loss
        + 10 * path_loss_exponent
        * np.log10(distances / reference_distance)
    )

    return path_loss
# -----------------------------
# Channel Gain
# -----------------------------

def calculate_channel_gain(path_loss):
    """
    Convert path loss from dB to linear channel gain.
    """

    channel_gain = 10 ** (-path_loss / 10)

    return channel_gain
# -----------------------------
# Received Power
# -----------------------------

def calculate_received_power(transmit_power, channel_gain):
    """
    Calculate received power using transmit power
    and channel gain.
    """

    received_power = transmit_power * channel_gain

    return received_power
# -----------------------------
# SINR
# -----------------------------

def calculate_sinr(received_power, noise_power):
    """
    Calculate Signal-to-Noise Ratio (SNR).
    Since interference is not modeled yet,
    SNR is used as a simplified SINR.
    """

    sinr = received_power / noise_power

    return sinr
# -----------------------------
# Throughput
# -----------------------------

def calculate_throughput(sinr, bandwidth):
    """
    Calculate theoretical throughput using
    the Shannon capacity formula.
    """

    throughput = bandwidth * np.log2(1 + sinr)

    return throughput