#!/usr/bin/env bash
MODELRUN=$1
RESULTS="results\/$MODELRUN"
echo $RESULTS
mkdir results/$MODELRUN
mkdir processed_data/$MODELRUN
cat model/model.txt > processed_data/$MODELRUN/osemosys.txt
sed -i '' "s/res\/csv/$RESULTS/g" processed_data/$MODELRUN/osemosys.txt
