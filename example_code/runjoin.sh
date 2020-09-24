#!/bin/bash
filename="hostfile-sorted.txt"
c_file="constant.txt"

node=$(head -n +1 "$filename") 
constant=$(head -n +1 "$c_file")

ssh -f "$node python3 $PWD/christer.py -c True -j $constant:5231"

tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"
