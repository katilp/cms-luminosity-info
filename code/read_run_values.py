#!/usr/bin/env python

import subprocess
import sys

"""
Read run range information from an input file.
"""

input = sys.argv[1]
if "Run" in input:
    run_period = input
else:
    year = input



def read_run_range(run_period):
    """Read run range for the given run period."""

    run_range = []
    with open("./inputs/run_ranges_run2.txt", "r") as f:
        for line in f.readlines():
            if line.split(",")[0] == run_period:                
              run_range.append(line.split(",")[1].strip())
              run_range.append(line.split(",")[2].strip())
    return run_range

def main():
    "Do the job."

    print (*read_run_range(run_period), sep =', ')

if __name__ == "__main__":
    main()
