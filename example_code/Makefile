TARGS = compute hostfile createmany createone join
m = 16

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

clean:
	rm -f compute.txt
	rm -f constant.txt
	rm -f hostfile-random.txt
	rm -f hostfile-sorted.txt


