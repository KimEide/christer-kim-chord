node1=compute-8-12
node2=compute-6-16
node3=compute-3-25
node4=compute-3-10
node5=compute-2-2

port=53464

ssh $node1 python3 $PWD/christer.py -p $port -c True $node2:$port $node5:$port &
ssh $node2 python3 $PWD/christer.py -p $port -c True $node3:$port $node1:$port &
ssh $node3 python3 $PWD/christer.py -p $port -c True $node4:$port $node2:$port &
ssh $node4 python3 $PWD/christer.py -p $port -c True $node5:$port $node3:$port &
ssh $node5 python3 $PWD/christer.py -p $port -c True $node1:$port $node4:$port 
