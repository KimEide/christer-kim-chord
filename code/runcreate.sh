#!/bin/bash
#create the first node in the chordprotocol.

/share/apps/ifi/available-nodes.sh | grep compute | shuf | tail -n +2 > compute.txt
m=16
python3 genhostfile.py $m

filename="hostfile-sorted.txt"
file_to_write="constant.txt"

node=$(head -n +1 "$filename") 
echo $node > "$file_to_write"
 
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

ssh -f $node "python3 $PWD/node.py -c True -p 5231"
