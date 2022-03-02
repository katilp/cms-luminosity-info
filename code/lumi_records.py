#!/usr/bin/env python

import json
import datetime
import subprocess
import requests
from helpers import *
import pandas as pd


"""
Create a luminosity record.
"""

RECID_START = 1055
YEAR_RELEASED = 2015



def create_record(recid, year, uncertainty, lumi_ref, val_recid):
    """Create record for the given year."""

    rec = {}

    year_created = year
    year = str(year)
    year_published = datetime.date.today().strftime("%Y")
    # NB the reference needs to be to cds for this to work:
    url = lumi_ref+'/?of=tm&ot=245__a'
    lumi_ref_title = requests.get(url).text.strip()

    rec["abstract"] = {}

    rec["abstract"]["description"] = (
            "<p>CMS measures the luminosity using different luminometers (luminosity detectors) and algorithms. The luminometer giving the best value for each luminosity section is recorded in a 'normtag' file that is used in the luminosity calculation.</p>"
            + "<p>The integrated luminosity for validated runs and luminosity sections of the %s public data (%s) is available in %slumi.txt (The integrated luminosity for validated runs and luminosity sections of all %s p-p data taking is available in %slumi.txt.)</p>" % (year, ",".join(read_run_periods(year, 'od')),  ",".join(read_run_periods(year, 'od')), year, year)
            + "<p> For luminosity calculation, a detailed list of luminosity by lumi section is provided in <a href=\"/record/%s/files/%slumibyls.csv\">%slumibyls.csv</a> for the <a href=\"/record/%s\">list of validated runs</a> and lumi sections.</p>" % (recid, year, year, val_recid)
            + "<p>The uncertainty in the luminosity measurement of %s data should be considered as %s%%(reference <a href=\"%s\">%s</a>).</p>" % (year, uncertainty, lumi_ref, lumi_ref_title)
            + "<p>In your estimate for the integrated luminosity, check for which runs the trigger you have selected is active and sum the values for those runs. If you are using prescaled triggers, you can find the trigger prescale factors as shown in <a href=\"/record/5004\">the trigger examples</a>.</p>"
            + "<p>Additional information on how to extract luminosity values using the <strong>brilcalc tool</strong> can be found in the <a href=\"/docs/cms-guide-luminosity-calculation\"> luminosity calculation guide</a>.</p>"
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

    rec["links"] = {}
    rec["links"]["url"] = lumi_ref
    rec["links"]["title"] = lumi_ref_title

    rec["publisher"] = "CERN Open Data Portal"

    rec["recid"] = str(recid)

    rec["relations"] = {}
    rec["relations"]["recid"] = val_recid
    rec["relations"]["type"] = "isRelatedTo"


    rec["run_period"] = read_run_periods(year, 'all')

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


    all_years = pd.read_json('./inputs/cms_release_info.json')
    released_years = all_years[all_years["year"] <= float(YEAR_RELEASED)] 

    for index, row in released_years.iterrows():
        records.append(
            create_record(
                recid,
                row["year"],
                row["lumi_uncertainty"],
                row["luminosity_reference"],
                row["val_json"][0]["recid"]) # This requires the json files to be in a specific order, with "golden" first
        )
        recid += 1



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

