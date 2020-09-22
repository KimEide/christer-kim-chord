ssh compute-6-7  python3 $PWD/kim.py -p 64500 compute-6-12:64500 compute-6-10:64500 &
ssh compute-6-12 python3 $PWD/kim.py -p 64500 compute-6-9:64500 compute-6-7:64500 &
ssh compute-6-9 python3 $PWD/kim.py -p 64500 compute-6-11:64500 compute-6-12:64500 &
ssh compute-6-11 python3 $PWD/kim.py -p 64500 compute-6-10:64500 compute-6-9:64500 &
ssh compute-6-10 python3 $PWD/kim.py -p 64500 compute-6-7:64500 compute-6-11:64500
