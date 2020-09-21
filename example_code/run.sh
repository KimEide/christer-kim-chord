# python3 dummynode.py -p 8000 localhost:8009 localhost:8001 & denne
python3 dummynode.py -p 8002 localhost:8006 localhost:8012 & 
python3 dummynode.py -p 8006 localhost:8008 localhost:8002 & 
python3 dummynode.py -p 8008 localhost:8010 localhost:8006 & 
python3 dummynode.py -p 8010 localhost:8012 localhost:8008 &
python3 dummynode.py -p 8012 localhost:8002 localhost:8010 #& denne
#
# python3 dummynode.py -p 8002 localhost:8001 localhost:8003 #&
#python3 dummynode.py -p 8003 localhost:8001 localhost:8004 & 
# python3 dummynode.py -p 8004 localhost:8003 localhost:8005 & 
# python3 dummynode.py -p 8005 localhost:8004 localhost:8006 & 
# python3 dummynode.py -p 8006 localhost:8005 localhost:8007 & 
# python3 dummynode.py -p 8007 localhost:8006 localhost:8008 & 
# python3 dummynode.py -p 8008 localhost:8007 localhost:8009 & 
# python3 dummynode.py -p 8009 localhost:8008 localhost:8000 