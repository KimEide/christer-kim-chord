# python3 dummynode.py -p 8000 localhost:8009 localhost:8001 & denne
python3 christer.py -p 8001 localhost:8002 localhost:8003 & 
python3 christer.py -p 8002 localhost:8016 localhost:8001 & 
python3 christer.py -p 8016 localhost:8009 localhost:8002 & 
python3 christer.py -p 8009 localhost:8003 localhost:8016 &
python3 christer.py -p 8003 localhost:8001 localhost:8009 #& denne
#
# python3 dummynode.py -p 8002 localhost:8001 localhost:8003 #&
#python3 dummynode.py -p 8003 localhost:8001 localhost:8004 & 
# python3 dummynode.py -p 8004 localhost:8003 localhost:8005 & 
# python3 dummynode.py -p 8005 localhost:8004 localhost:8006 & 
# python3 dummynode.py -p 8006 localhost:8005 localhost:8007 & 
# python3 dummynode.py -p 8007 localhost:8006 localhost:8008 & 
# python3 dummynode.py -p 8008 localhost:8007 localhost:8009 & 
# python3 dummynode.py -p 8009 localhost:8008 localhost:8000 