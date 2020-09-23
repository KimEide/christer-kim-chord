TARGS = compute hostfile create join
m = 16

all: $(TARGS)

compute: 
	bash getcompute.sh

hostfile:
	python3 genhostfile.py $m

create:
	bash runcreate.sh

join:
	bash runjoin.sh


clean:
	rm -f compute.txt
	rm -f constant.txt
	rm -f hostfile-random.txt
	rm -f hostfile-sorted.txt


