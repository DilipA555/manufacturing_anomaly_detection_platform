def format_alert_message(machine_id: str, sector: str, parameter: str, value: float) -> str:
    """Generate a readable alert message"""

    return (
        f"ALERT: {parameter.upper()} anomaly in Machine {machine_id} "
        f"({sector}) with value {value}"
    )