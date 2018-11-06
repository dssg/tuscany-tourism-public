#!/bin/bash

start_time="$(date -u +%s)"

for file in configs/*.json
do
	echo starting clustering
	Rscript sequence_clustering.R "$file"
done

end_time="$(date -u +%s)"

elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for process"
