"""Parser for KACO inverter hex response data."""
from __future__ import annotations

import struct


def to_little_32_float(hex_string: str) -> float:
    """Convert 8 hex chars (little-endian 32-bit) to float."""
    return struct.unpack("<f", bytes.fromhex(hex_string))[0]


def to_little_32_int(hex_string: str) -> int:
    """Convert 8 hex chars (little-endian 32-bit) to unsigned int."""
    return struct.unpack("<I", bytes.fromhex(hex_string))[0]


def _find_last_occurrence(data: str, pattern: str) -> int | None:
    """Find the last occurrence of pattern in data (search starts at index 1)."""
    pos = None
    start = 1
    while True:
        found = data.find(pattern, start)
        if found == -1:
            break
        pos = found
        start = found + 4
    return pos


def extract_32bit_float(data: str, address: str) -> float | None:
    """Extract a 32-bit little-endian float at the given address marker."""
    pos = _find_last_occurrence(data, address)
    if pos is None:
        return None
    raw = data[pos + 8 : pos + 16]
    if len(raw) < 8:
        return None
    return to_little_32_float(raw)


def extract_96bit_float_array(
    data: str, address: str
) -> tuple[float, float, float] | None:
    """Extract three consecutive 32-bit little-endian floats."""
    pos = _find_last_occurrence(data, address)
    if pos is None:
        return None
    raw = data[pos + 8 : pos + 32]
    if len(raw) < 24:
        return None
    return (
        to_little_32_float(raw[0:8]),
        to_little_32_float(raw[8:16]),
        to_little_32_float(raw[16:24]),
    )


def extract_96bit_int_array(
    data: str, address: str
) -> tuple[int, int, int] | None:
    """Extract three consecutive 32-bit little-endian unsigned ints."""
    pos = _find_last_occurrence(data, address)
    if pos is None:
        return None
    raw = data[pos + 8 : pos + 32]
    if len(raw) < 24:
        return None
    return (
        to_little_32_int(raw[0:8]),
        to_little_32_int(raw[8:16]),
        to_little_32_int(raw[16:24]),
    )


def _try_float(result: dict, hex_data: str, address: str, key: str) -> None:
    """Helper: extract a 32-bit float and store in result if found."""
    if address in hex_data:
        val = extract_32bit_float(hex_data, address)
        if val is not None:
            result[key] = round(val)


def parse_inverter_data(hex_data: str) -> dict:
    """Parse the combined hex response from the inverter.

    Returns a dict containing only the values found in this response.
    Derived values (totals, consumption) are NOT computed here.
    """
    result: dict = {}

    # 32-bit float values
    _try_float(result, hex_data, "04005c7c", "power_inv_l1")
    _try_float(result, hex_data, "04007b7c", "power_inv_l2")
    _try_float(result, hex_data, "04009a7c", "power_inv_l3")
    _try_float(result, hex_data, "0400bcca", "u_pv_1")
    _try_float(result, hex_data, "0400dbca", "u_pv_2")
    _try_float(result, hex_data, "04005396", "p_pv")
    _try_float(result, hex_data, "0400e9d2", "u_bat")
    _try_float(result, hex_data, "04005e89", "p_bat")
    _try_float(result, hex_data, "0400a7d3", "soc_bat")
    _try_float(result, hex_data, "04007dfe", "temp_inverter")
    _try_float(result, hex_data, "040073e3", "bat_cycles")

    # Net power per phase (96-bit float array = 3 × 32-bit float)
    if "0c00b395" in hex_data:
        vals = extract_96bit_float_array(hex_data, "0c00b395")
        if vals is not None:
            result["power_net_l1"] = round(vals[0])
            result["power_net_l2"] = round(vals[1])
            result["power_net_l3"] = round(vals[2])

    # Energy counters (96-bit int arrays)
    if "0c003454" in hex_data:
        vals = extract_96bit_int_array(hex_data, "0c003454")
        if vals is not None:
            result["today_grid_feed_in"] = round(vals[0] / 274 * 10, 1)
            result["this_month_grid_feed_in"] = round(vals[1] * 1.1, 1)

    if "0c00c27c" in hex_data:
        vals = extract_96bit_int_array(hex_data, "0c00c27c")
        if vals is not None:
            result["today_cons_from_grid"] = round(vals[0] / 274 * 10, 1)
            result["this_month_cons_from_grid"] = round(vals[1] * 1.1, 1)

    if "0c002255" in hex_data:
        vals = extract_96bit_int_array(hex_data, "0c002255")
        if vals is not None:
            result["today_cons_self"] = round(vals[0] / 274, 1)
            result["this_month_today_cons_self"] = round(vals[1] * 1.1 / 10, 1)

    if "0c00c5a0" in hex_data:
        vals = extract_96bit_int_array(hex_data, "0c00c5a0")
        if vals is not None:
            result["today_battery_energy_volume"] = round(vals[0] / 274, 1)
            result["this_month_battery_energy_volume"] = round(vals[1] * 1.1 / 10, 1)

    return result
