TARGS = compute hostfile createmany createone join client
m = 16
constant=$(head -n +1 $"constant.txt")

all: $(TARGS)

compute: 
	bash getcompute.sh

hostfile:
	python3 genhostfile.py $m

createmany:
	bash runcluster.sh

createone:
	bash runcreate.sh

join:
	bash runjoin.sh

client:s
	python3 client.py $constant:8000

clean:
	rm -f compute.txt
	rm -f constant.txt
	rm -f hostfile-random.txt
	rm -f hostfile-sorted.txt


