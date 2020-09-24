node1=compute-6-9
node2=compute-6-9
node3=compute-6-9
node4=compute-6-9
node5=compute-6-9

port=53464

python3 $PWD/christer.py -p 8000 -c True $node2:8001 $node5:8004 &
python3 $PWD/christer.py -p 8001 -c True $node3:8002 $node1:8000 &
python3 $PWD/christer.py -p 8002 -c True $node4:8003 $node2:8001 &
python3 $PWD/christer.py -p 8003 -c True $node5:8004 $node3:8002 &
python3 $PWD/christer.py -p 8004 -c True $node1:8000 $node4:8003 
