#!/usr/bin/env python

import json
import datetime
import requests

import sys
sys.path.insert(1, '../cms-release-info')

"""
Create a luminosity record.
"""

# May 2023, the last recid 1055 for 2015 pp:

### input for 2013 pPb
#
#RECID_START = 1056
#YEAR_RELEASED = 2013
#RUN_ERA = "HIRun2013"
#TYPE = "pPb"
#
### input for 2013 ppref
#
RECID_START = 1057
YEAR_RELEASED = 2013
RUN_ERA = "Run2013A"
TYPE = "pphiref"

### input for already released 2015, taken into account the updates in the scripts for collision type 
#
#RECID_START = 1055
#YEAR_RELEASED = 2015
#RUN_ERA = "Run2016H" # single era defined only to get the collision energy, stored per era
#TYPE = "pp"



def create_record(recid, year, era, runtype, uncertainty, lumi_ref, val_recid):
    """Create record for the given year."""

    rec = {}

    year = str(year)
    year_created = year
    year_published = datetime.date.today().strftime("%Y")
    runtype = str(runtype)
    if "pphiref" in runtype :
        display_runtype = 'pp'
    else:
        display_runtype = runtype
        
    # Get the energy
    # Using the run_era, for pp it is needed only here
    # Could be done differently but this is good enough
    url = 'http://api-server-cms-release-info.app.cern.ch/runeras/?run_era='+era
    this_json=json.loads(requests.get(url).text.strip())
    energy=this_json[0]["energy"]

    # NB the reference needs to be to cds for this to work:
    url = lumi_ref+'/?of=tm&ot=245__a'
    lumi_ref_title = requests.get(url).text.strip()

    if "pphiref" in runtype:
        collision_text = energy+' proton-proton collision data, needed as reference data for heavy-ion data analysis,'
    elif "PbPb" in runtype:
        collision_text = energy+' PbPb heavy-ion collision data'
    elif "pPb" in runtype:
        collision_text = energy+' proton-Pb heavy-ion collision data'
    elif "pp" in runtype:
        collision_text = energy+' proton-proton collision data'
        run_range_input = year
    else:
        print('Runtype unknown!')

    rec["abstract"] = {}

    url = 'http://api-server-cms-release-info.app.cern.ch/runeras/run_era?year='+year+'&type='+type+'-phys&released=yes'
    od_runs = json.loads(requests.get(url).text.strip())

    rec["abstract"]["description"] = (
            "<p>CMS measures the luminosity using different luminometers (luminosity detectors) and algorithms. The luminometer giving the best value for each luminosity section is recorded in a 'normtag' file <a href=\"/record/%s/files/normtag_PHYSICS_%s.json\">normtag_PHYSICS_%s.json</a> that is used in the luminosity calculation.</p>" % (recid, year, year)
            + "<p>The integrated luminosity for validated runs and luminosity sections of the %s public data (%s) is available in %slumi.txt. (The integrated luminosity for validated runs and luminosity sections of all %s p-p data taking is available in %slumi.txt.)</p>" % (year, ",".join(od_runs), ",".join(od_runs), year, year)
            + "<p> For luminosity calculation, a detailed list of luminosity by lumi section is provided in <a href=\"/record/%s/files/%slumibyls.csv\">%slumibyls.csv</a> for the <a href=\"/record/%s\">list of validated runs</a> and lumi sections.</p>" % (recid, year, year, val_recid)
            + "<p>The uncertainty in the luminosity measurement of %s data should be considered as %s%% (reference <a href=\"%s\">%s</a>).</p>" % (year, uncertainty, lumi_ref, lumi_ref_title)
            + "<p>In your estimate for the integrated luminosity, check for which runs the trigger you have selected is active and sum the values for those runs. If you are using prescaled triggers, you can find the trigger prescale factors as shown in <a href=\"/record/5004\">the trigger examples</a>. The change of prescales (run, lumi section, index of prescales) is recorded in <a href=\"/record/%s/files/prescale%s.csv\">prescale%s.csv</a></p>" % (recid, year, year)
            + "<p>Additional information on how to extract luminosity values using the <strong>brilcalc tool</strong> can be found in the <a href=\"/docs/cms-guide-luminosity-calculation\"> luminosity calculation guide</a>.</p>"
        )

    rec["accelerator"] = "CERN-LHC"

    rec["collaboration"] = {}
    rec["collaboration"]["name"] = "CMS collaboration"

    rec["collections"] = [
        "CMS-Luminosity-Information",
    ]

    rec["collision_information"] = {}
    rec["collision_information"]["energy"] = energy
    rec["collision_information"]["type"] = display_runtype

    rec["date_created"] = [
        year_created,
    ]
    rec["date_published"] = year_published

    rec["experiment"] = "CMS"

    rec["license"] = {}
    rec["license"]["attribution"] = "CC0"

    rec["links"] = {}
    rec["links"] = [
        {
            "url": lumi_ref,
            "title": lumi_ref_title
        }
    ]   

    rec["publisher"] = "CERN Open Data Portal"

    rec["recid"] = str(recid)

    rec["relations"] = {}
    rec["relations"] = [
        {
            "recid": str(val_recid),
            "type": "isRelatedTo"
        }
    ]

    url = 'http://api-server-cms-release-info.app.cern.ch/runeras/run_era?year='+year+'&type=pp-phys'
    #rec["run_period"] = read_run_periods(year, 'pp-phys')
    rec["run_period"] = json.loads(requests.get(url).text.strip())

    rec["title"] = (
        "CMS luminosity information for "+collision_text+" taken in "+year
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
    year = str(YEAR_RELEASED)
    era = str(RUN_ERA)
    runtype = str(TYPE)

    # this would read from the local json file
    # with open('./inputs/cms_release_info.json') as f:
    #      data = f.read()
    
    # # reconstructing the data as a dictionary
    # all_years = json.loads(data)    
    # this_year = all_years[year]

    # this gets json from the api server
    url = 'http://api-server-cms-release-info.app.cern.ch/years?year='+year+'&type='+runtype+'&output=plain'
    this_year = json.loads(requests.get(url).text.strip())
    
    records.append(
        create_record(
            recid,
            this_year["year"],
            era,
            runtype,            
            this_year["lumi_uncertainty"],
            this_year["luminosity_reference"],
            this_year["val_json"][0]["recid"]) # This requires the json files to be in a specific order, with "golden" first
    )



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

