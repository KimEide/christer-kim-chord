filename="hostfile-random.txt"
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

ssh $node1 python3 $PWD/christer.py -p 5231 -c True $node2:5231 $node5:5231 &
ssh $node2 python3 $PWD/christer.py -p 5231 -c True $node3:5231 $node1:5231 &
ssh $node3 python3 $PWD/christer.py -p 5231 -c True $node4:5231 $node2:5231 &
ssh $node4 python3 $PWD/christer.py -p 5231 -c True $node5:5231 $node3:5231 &
ssh $node5 python3 $PWD/christer.py -p 5231 -c True $node1:5231 $node4:5231 

# python3 christer.py -p 5231 -c True $node2:5229 $node5:5211 &
# python3 christer.py -p 5232 -c True $node3:5226 $node1:5212 &
# python3 christer.py -p 5233 -c True $node4:5225 $node2:5213 &
# python3 christer.py -p 5234 -c True $node5:5224 $node3:5214 &
# python3 christer.py -p 5235 -c True $node1:5223 $node4:5216 

#ssh compute-7-7 python3 $PWD/christer.py -p 5231 -c True

