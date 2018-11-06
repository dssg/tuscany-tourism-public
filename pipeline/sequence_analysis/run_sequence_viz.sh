#!/bin/bash

start_time="$(date -u +%s)"

for file in configs/*.json
do
	python3 sequence_vizualization.py "$file"& 
done

end_time="$(date -u +%s)"

elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for process"
