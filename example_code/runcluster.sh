filename="hostfile-sorted.txt"
file_to_write="constant.txt"

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

# ssh $node1 python3 $PWD/kim.py -p 64500 $node2:64500 $node5:64500 &
# ssh $node2 python3 $PWD/kim.py -p 64500 $node3:64500 $node1:64500 &
# ssh $node3 python3 $PWD/kim.py -p 64500 $node4:64500 $node2:64500 &
# ssh $node4 python3 $PWD/kim.py -p 64500 $node5:64500 $node3:64500 &
# ssh $node5 python3 $PWD/kim.py -p 64500 $node1:64500 $node4:64500

ssh $node1 python3 $PWD/christer.py -p 5231 $node2:5231 $node5:5231 &
ssh $node2 python3 $PWD/christer.py -p 5231 $node3:5231 $node1:5231 &
ssh $node3 python3 $PWD/christer.py -p 5231 $node4:5231 $node2:5231 &
ssh $node4 python3 $PWD/christer.py -p 5231 $node5:5231 $node3:5231 &
ssh $node5 python3 $PWD/christer.py -p 5231 $node1:5231 $node4:5231 

