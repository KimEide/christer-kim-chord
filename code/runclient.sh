c_file="constant.txt"
constant=$(head -n +1 $"constant.txt") 

python3 client.py $constant:5231