node1=$(head -n +1 $"hostfile-sorted.txt")
tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"
node2=$(head -n +1 $"hostfile-sorted.txt")
tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"
node3=$(head -n +1 $"hostfile-sorted.txt")
tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"
node4=$(head -n +1 $"hostfile-sorted.txt")
tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"
node5=$(head -n +1 $"hostfile-sorted.txt")
tail -n +2 $"hostfile-sorted.txt" > $"FILE.tmp" && mv $"FILE.tmp" $"hostfile-sorted.txt"

# ssh $node1 python3 $PWD/kim.py -p 64500 $node2:64500 $node5:64500 &
# ssh $node2 python3 $PWD/kim.py -p 64500 $node3:64500 $node1:64500 &
# ssh $node3 python3 $PWD/kim.py -p 64500 $node4:64500 $node2:64500 &
# ssh $node4 python3 $PWD/kim.py -p 64500 $node5:64500 $node3:64500 &
# ssh $node5 python3 $PWD/kim.py -p 64500 $node1:64500 $node4:64500

ssh $node1 python3 $PWD/christer.py -p 64500 $node2:64500 $node5:64500 &
ssh $node2 python3 $PWD/christer.py -p 64500 $node3:64500 $node1:64500 &
ssh $node3 python3 $PWD/christer.py -p 64500 $node4:64500 $node2:64500 &
ssh $node4 python3 $PWD/christer.py -p 64500 $node5:64500 $node3:64500 &
ssh $node5 python3 $PWD/christer.py -p 64500 $node1:64500 $node4:64500

$node1 > $"constant.txt" 
