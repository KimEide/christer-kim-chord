#!/bin/bash
node=$(head -n +1 $"hostfile-sorted.txt")

echo ssh -f $node '"'python3 "$"PWD/christer-kim/example_code/christer.py -c True -j $node:8000'"'

tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"
