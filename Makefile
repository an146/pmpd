test:
	./pmpd.py stop || true
	./pmpd.py start
	sleep 1
	./pmpc.py play rad
