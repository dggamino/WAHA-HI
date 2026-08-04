from observability.report import DiagnosticReport



def main():

    report = DiagnosticReport()


    print(
        "=== WAHA-HI SYSTEM DIAGNOSTICS ==="
    )


    result = report.generate()


    print("")

    print(
        "HEALTH:"
    )

    print(
        result["health"]
    )


    print("")

    print(
        "METRICS:"
    )

    print(
        result["metrics"]
    )


    print("")

    print(
        "EVENTS:"
    )

    for event in result["recent_events"]:

        print(event)



if __name__ == "__main__":

    main()
