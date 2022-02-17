#!/bin/bash -l
# parameters: $1 
# exit on error
set -e

if [ -z "$1" ]; then runmin=256630; else runmin=$1; fi
if [ -z "$2" ]; then runmax=260627; else runmax=$2; fi
if [ -z "$3" ]; then cert=Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt; else cert=$3; fi

brilcalc lumi -c web --begin $runmin --end $runmax -i $cert

