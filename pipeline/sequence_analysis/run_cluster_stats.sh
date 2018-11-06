#!/bin/bash

start_time="$(date -u +%s)"

for file in configs/*.json
do

	Rscript save_cluster_stats.R "$file" &

done

end_time="$(date -u +%s)"

elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for process"
