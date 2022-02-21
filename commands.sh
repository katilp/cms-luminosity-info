#!/bin/bash -l
# parameters: $1 
# exit on error
set -e

cert=$1
if [  -z "$2" ]
then
  brilcalc lumi -c web -i /mnt/vol/$cert -u /fb --normtag /mnt/vol/inputs/normtag_PHYSICS.json
elif [ -z "$3" ]
then
  echo "Give maximum range" 
else
  runmin=$2
  runmax=$3
  brilcalc lumi -c web --begin $runmin --end $runmax -i /mnt/vol/$cert -u /fb --normtag /mnt/vol/inputs/normtag_PHYSICS.json
fi
