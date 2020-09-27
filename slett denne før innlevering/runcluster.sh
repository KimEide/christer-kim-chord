/share/apps/ifi/available-nodes.sh | grep compute | shuf | tail -n +2 > compute.txt

m=16

python3 genhostfile.py $m

filename="hostfile-random.txt"
file_to_write="constant.txt"
port=5231

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

ssh $node1 python3 $PWD/christer.py -p $port -c True $node2:$port $node5:$port &
sleep .05
ssh $node2 python3 $PWD/christer.py -p $port -c True $node3:$port $node1:$port &
sleep .05
ssh $node3 python3 $PWD/christer.py -p $port -c True $node4:$port $node2:$port &
sleep .05
ssh $node4 python3 $PWD/christer.py -p $port -c True $node5:$port $node3:$port &
sleep .05
ssh $node5 python3 $PWD/christer.py -p $port -c True $node1:$port $node4:$port 
