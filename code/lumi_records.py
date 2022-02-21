#!/usr/bin/env python

import json
import datetime
import subprocess

"""
Create Run-2 luminosity records.
"""

RECID_START = 1055


# def create_summary_files(year):
#     summary_files = []
    
#     s = subprocess.check_output('docker ps -a', shell=True)
#     if s contains brilws:
        

#     return summary_files

def read_run_periods(year):
    """Read run periods for the given year."""

    run_periods = []
    with open("./inputs/run_ranges_run2.txt", "r") as f:
        for line in f.readlines():
            run_period = line.split(",")[0]
            if year in run_period:
                run_periods.append(run_period)
    return run_periods


def create_record(recid, year, uncertainty, lumi_ref):
    """Create record for the given year."""

    rec = {}

    year_created = year
    year_published = datetime.date.today().strftime("%Y")
    year_published = "2022"

    rec["abstract"] = {}

    rec["abstract"]["description"] = (
            "<p>"
            + "CMS measures the luminosity using different luminometers (luminosity detectors) and algorithms. %s"
            % year
            + "</p><p>Some other text</p>"
        )

    rec["accelerator"] = "CERN-LHC"

    rec["collaboration"] = {}
    rec["collaboration"]["name"] = "CMS collaboration"

    rec["collections"] = [
        "CMS-Luminosity-Information",
    ]

    rec["collision_information"] = {}
    rec["collision_information"]["energy"] = "13TeV"
    rec["collision_information"]["type"] = "pp"

    rec["date_created"] = [
        year_created,
    ]
    rec["date_published"] = year_published

    rec["experiment"] = "CMS"

    rec["license"] = {}
    rec["license"]["attribution"] = "CC0"

    rec["publisher"] = "CERN Open Data Portal"

    rec["recid"] = str(recid)

    rec["run_period"] = read_run_periods(year)

    rec["title"] = (
        "CMS luminosity information, for %s CMS open data"
        % year
        )

    rec["type"] = {}
    rec["type"]["primary"] = "Supplementaries"
    rec["type"]["secondary"] = [
        "Luminosity",
    ]

    return rec

# @click.command()
def main():
    "Do the job."

    records = []
    recid = RECID_START
    with open("./inputs/lumi_info.txt", "r") as f:
        for info_line in f.readlines():
            year = info_line.split(",")[0]
            uncertainty = info_line.split(",")[1]
            lumi_ref = info_line.split(",")[2]
            records.append(
                create_record(recid, year, uncertainty, lumi_ref)
            )
            recid += 1

            # create_summary_files(year)

    print(
        json.dumps(
            records,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ": "),
        )
    )


if __name__ == "__main__":
    main()

