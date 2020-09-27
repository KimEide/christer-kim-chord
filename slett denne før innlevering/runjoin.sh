#!/bin/bash
filename="hostfile-random.txt"
c_file="constant.txt"

node=$(head -n +1 "$filename") 
constant=$(head -n +1 "$c_file")

tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

ssh -f $node "python3 $PWD/christer.py -p 5231 -c True -j $constant:5231"

