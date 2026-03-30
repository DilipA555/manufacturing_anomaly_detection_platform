from datetime import datetime
from typing import Union


def format_alert_message(
    machine_id: str,
    sector: str,
    param: str,
    value: Union[int, float],
    timestamp: datetime
) -> str:
    """
    Format alert message for logging

    Args:
        machine_id (str): Machine identifier
        sector (str): Sector name
        param (str): Parameter causing anomaly
        value (int | float): Detected value
        timestamp (datetime): Original data timestamp

    Returns:
        str: Formatted alert log string
    """

    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"{formatted_time} | Machine: {machine_id} | Sector: {sector} | "
        f"Parameter: {param} | Value: {round(value, 2)}"
    )