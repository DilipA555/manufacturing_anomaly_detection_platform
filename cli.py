import cProfile
from main import run_pipeline

if __name__ == "__main__":
    print("=== MANUFACTURING ANOMALY DETECTION PLATFORM ===\n")

    profiler = cProfile.Profile()
    profiler.enable()

    result = run_pipeline()

    profiler.disable()

    # display
    processed_data = result["processed_data"]
    anomalies = result["anomalies"]
    alerts = result["alerts"]
    recent_alerts = result["recent_alerts"]
    analytics_data = result["analytics_data"]
    current, peak = result["memory"]

    print("=== SYSTEM SUMMARY ===")
    print(f"Total records processed: {len(processed_data)}")
    print(f"Total anomalies detected: {len(anomalies)}")
    print(f"Total alerts generated: {len(alerts)}")

    print("\n=== RECENT ALERTS ===")
    for alert in recent_alerts:
        print(
            f"Machine: {alert['machine_id']} | "
            f"Sector: {alert['sector']} | "
            f"Type: {alert['anomaly_type']} | "
            f"Value: {round(alert['value'], 2)} | "
            f"Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
        )

    # analytics
    sector_totals = {}
    sector_parameter_breakdown = {}

    for sector, parameter, count in analytics_data:
        sector_totals[sector] = sector_totals.get(sector, 0) + count

        if sector not in sector_parameter_breakdown:
            sector_parameter_breakdown[sector] = {}

        sector_parameter_breakdown[sector][parameter] = count

    print("\n=== SECTOR SUMMARY ===")
    for sector, total in sector_totals.items():
        print(f"{sector}: {total}")

    print("\n=== PARAMETER BREAKDOWN ===")
    for sector, parameters in sector_parameter_breakdown.items():
        print(f"\n{sector}:")
        for parameter, count in parameters.items():
            print(f"   {parameter}: {count}")

    print(f"\nMemory Usage: {current / 10**6:.2f} MB")
    print(f"Peak Memory Usage: {peak / 10**6:.2f} MB")

    print("\nExecution Completed")

    # profile output
    print("\n=== PERFORMANCE PROFILE ===")
    profiler.print_stats(sort="cumtime")