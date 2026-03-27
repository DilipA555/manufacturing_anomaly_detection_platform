def format_alert_message(machine_id, sector, parameter, value):
    """Generate a readable alert message"""

    return (
        f"ALERT: {parameter.upper()} anomaly in Machine {machine_id} "
        f"({sector}) with value {value}"
    )