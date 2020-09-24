#!/bin/bash
#create the first node in the chordprotocol.
filename="hostfile-sorted.txt"
file_to_write="constant.txt"

node=$(head -n +1 "$filename") 
echo $node > "$file_to_write" 

ssh $node python3 "$"PWD/christer-kim/example_code/christer.py -c True -p 5231

tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"


#ssh -f compute-7-7 "python3 $PWD/christer-kim/example_code/christer.py -p 8012
#ssh -f compute-3-15 "python3 /home/christer/Desktop/christer-kim/example_code/christer-kim/example_code/christer.py -c True -j compute-3-15:8000"
