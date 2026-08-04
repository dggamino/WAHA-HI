"""
CLI Dashboard
"""


from dashboard.service import DashboardService



def main():

    dashboard = DashboardService()


    report = dashboard.snapshot()


    print(
        "=== WAHA-HI OPERATIONAL DASHBOARD ==="
    )


    print("")

    print(
        "MODULES:"
    )

    print(
        report["health"]
    )


    print("")

    print(
        "METRICS:"
    )

    print(
        report["metrics"]
    )


    print("")

    print(
        "RECENT EVENTS:"
    )


    for event in report["recent_events"]:

        print(event)



if __name__ == "__main__":

    main()
