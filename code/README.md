# Run locally
use the runlocal.sh to run local, the client can be connected towards localhost:8007
This script uses a kill command to shutdown whatever runs on the same ports as the script runs on before it starts, which requires a password. 

To start:

bash runlocal.sh

python3 client.py localhost:8007

# Run on cluster
There are two different approaches to run it on the cluster, both of them starts on one node, and then joins later on.
There is a makefile, which only runs the bash scripts.

To start 5 nodes at the same time, use the 
make createmany or bash runcluster.sh command

To start on 1 node, use the
make createone or bash runcreate.sh

To join a node use
make join or bash runjoin.sh

To start the provided client use the 
make join or bash runclient.sh

to find which node to start a client on (the first node started)
cat constant.txt