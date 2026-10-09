
import numpy as np


def calculate_total_power(transmit_powers_mw, circuit_power_w=0.0):
    """
    Calculate total power consumption in watts.

    transmit_powers_mw: array of transmit powers in mW
    circuit_power_w: additional circuit power in watts
    """

    total_transmit_power_w = np.sum(transmit_powers_mw) / 1000

    total_power_w = total_transmit_power_w + circuit_power_w

    return total_power_w


def calculate_energy_consumption(total_power_w, duration_seconds):
    """
    Calculate energy consumption in joules.
    """

    energy_joules = total_power_w * duration_seconds

    return energy_joules


def calculate_energy_efficiency(total_throughput_bps, total_power_w):
    """
    Calculate energy efficiency in bits per joule.
    """

    if total_power_w <= 0:
        return 0.0

    return total_throughput_bps / total_power_w