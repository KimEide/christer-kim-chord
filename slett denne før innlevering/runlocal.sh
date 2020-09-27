#0:8007 1:8019 2:8010 3:8022 4:8036 5:8012 7:8014 8:8024 9:8026 10:8009 11:8049 12:8063 13:8015 15:8005
kill -9 $(sudo lsof -t -i:8007) 
kill -9 $(sudo lsof -t -i:8008) 
kill -9 $(sudo lsof -t -i:8019) 
kill -9 $(sudo lsof -t -i:8010) 
kill -9 $(sudo lsof -t -i:8022) 
kill -9 $(sudo lsof -t -i:8036) 
kill -9 $(sudo lsof -t -i:8012) 
kill -9 $(sudo lsof -t -i:8014) 
kill -9 $(sudo lsof -t -i:8024) 
kill -9 $(sudo lsof -t -i:8026) 
kill -9 $(sudo lsof -t -i:8009) 
kill -9 $(sudo lsof -t -i:8049) 
kill -9 $(sudo lsof -t -i:8063) 
kill -9 $(sudo lsof -t -i:8015) 
kill -9 $(sudo lsof -t -i:8005) 

python3 christer.py -p 8007 &
sleep 1
python3 christer.py -p 8019 -j localhost:8007 &
sleep 1
python3 christer.py -p 8010 -j localhost:8007 &
sleep 1
python3 christer.py -p 8022 -j localhost:8007 &
sleep 1
python3 christer.py -p 8036 -j localhost:8007 &
sleep 1
python3 christer.py -p 8012 -j localhost:8007 &
sleep 1
python3 christer.py -p 8014 -j localhost:8007 &
sleep 1
python3 christer.py -p 8024 -j localhost:8007 &
sleep 1
python3 christer.py -p 8026 -j localhost:8007 &
sleep 1
python3 christer.py -p 8009 -j localhost:8007 &
sleep 1
python3 christer.py -p 8049 -j localhost:8007 &
sleep 1
python3 christer.py -p 8063 -j localhost:8007 &
sleep 1
python3 christer.py -p 8015 -j localhost:8007 &
sleep 1
python3 christer.py -p 8005 -j localhost:8007 





