from datetime import datetime
from typing import Union, List, Tuple, Dict


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


def process_analytics_data(
    analytics_data: List[Tuple[str, str, int]]
) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    """aggregate anomaly counts per sector and parameter"""

    sector_totals: Dict[str, int] = {}
    sector_parameter_breakdown: Dict[str, Dict[str, int]] = {}

    for sector, parameter, count in analytics_data:
        sector_totals[sector] = sector_totals.get(sector, 0) + count

        if sector not in sector_parameter_breakdown:
            sector_parameter_breakdown[sector] = {}

        sector_parameter_breakdown[sector][parameter] = count

    return sector_totals, sector_parameter_breakdown