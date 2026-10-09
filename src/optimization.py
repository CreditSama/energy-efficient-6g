
import numpy as np


def allocate_dynamic_power(
    channel_gain,
    noise_power,
    bandwidth,
    target_rate_bps,
    min_power_mw=1.0,
    max_power_mw=100.0
):
    """
    Estimate the minimum transmit power needed
    to meet each user's target rate.

    Power values are returned in milliwatts.
    """

    # Convert the target rate into a required SNR.
    required_snr = 2 ** (target_rate_bps / bandwidth) - 1

    # Calculate required received power.
    required_received_power = required_snr * noise_power

    # Calculate required transmit power.
    required_power_mw = required_received_power / channel_gain

    # Apply minimum and maximum power limits.
    allocated_power_mw = np.clip(
        required_power_mw,
        min_power_mw,
        max_power_mw
    )

    return allocated_power_mw