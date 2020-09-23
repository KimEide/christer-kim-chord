#!/bin/bash
#create the first node in the chordprotocol.
node=$(head -n +1 $"hostfile-sorted.txt")
constant=$(head -n +1 $"constant.txt")

echo ssh -f $node '"'python3 "$"PWD/christer-kim/example_code/christer.py -c True -p $constant:8000'"'

$node > $"constant.txt" 
#ssh -f compute-7-7 "python3 $PWD/christer-kim/example_code/christer.py -p 8012
#ssh -f compute-3-15 "python3 /home/christer/Desktop/christer-kim/example_code/christer-kim/example_code/christer.py -c True -j compute-3-15:8000"
