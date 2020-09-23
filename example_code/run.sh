python3 dummynode.py -p 8002 localhost:8006 localhost:8012 & 
python3 dummynode.py -p 8006 localhost:8008 localhost:8002 & 
python3 dummynode.py -p 8008 localhost:8010 localhost:8006 & 
python3 dummynode.py -p 8010 localhost:8012 localhost:8008 &
python3 dummynode.py -p 8012 localhost:8002 localhost:8010 
