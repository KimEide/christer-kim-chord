/share/apps/ifi/available-nodes.sh | grep compute | shuf | tail -n +2 > compute.txt

m=32

python3 genhostfile.py $m

filename="hostfile-random.txt"
file_to_write="constant.txt"
port=62310

node1=$(head -n +1 "$filename") 
echo $node1 > "$file_to_write" 
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node2=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node3=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node4=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node5=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node6=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node7=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node8=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node9=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node10=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node11=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node12=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node13=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node14=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node15=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

node16=$(head -n +1 "$filename")
tail -n +2 "$filename" > "$filename.tmp" && mv "$filename.tmp" "$filename"

ssh $node1 python3 $PWD/node.py -p $port -c True  &
sleep .05
ssh $node2 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node3 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node4 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node5 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node6 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node7 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node8 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node9 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node10 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node11 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node12 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node13 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node14 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node15 python3 $PWD/node.py -p $port -c True -j $node1:$port &
sleep .05
ssh $node16 python3 $PWD/node.py -p $port -c True -j $node1:$port
