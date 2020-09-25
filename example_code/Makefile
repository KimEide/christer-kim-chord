TARGS = compute hostfile createmany createone join client
m = 16
c_file="constant.txt"
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

client:
	bash runclient.sh

clean:
	rm -f *.txt *.tmp

