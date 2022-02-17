#!/bin/sh -l
# exit on erro
set -e
sudo chown $USER /mnt/vol

brilcalc --help > my.out

cp *.out /mnt/vol/
