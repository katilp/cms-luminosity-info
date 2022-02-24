def read_run_periods(year, od):
    """Read run periods for the given year, if od yes, only those released."""

    run_periods = []
    with open("./inputs/run_ranges_run2.txt", "r") as f:
        for line in f.readlines():
            run_period = line.split(",")[0]
            opendata = line.split(",")[3]
            if year in run_period:
                if 'od' in od:
                    if 'yes' in opendata:
                        run_periods.append(run_period)
                else:
                    run_periods.append(run_period)
    return run_periods

def read_run_range(run_period):
    """Read run range for the given run period."""

    run_range = []
    with open("./inputs/run_ranges_run2.txt", "r") as f:
        for line in f.readlines():
            if line.split(",")[0] == run_period:                
              run_range.append(line.split(",")[1].strip())
              run_range.append(line.split(",")[2].strip())
    return run_range