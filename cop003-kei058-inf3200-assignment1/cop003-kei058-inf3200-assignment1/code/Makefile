TARGS = createmany createone join client
m = 16

all: $(TARGS)

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

