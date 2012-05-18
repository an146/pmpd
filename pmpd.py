import sys, time
from daemon import Daemon

def usage():
    print("usage: {0} start|stop|restart".format(sys.argv[0]))
    sys.exit(2)

class PmpdDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    daemon = PmpdDaemon(pidfile = '/tmp/pmpd.pid',
                        logfile = '/tmp/pmpd.log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            usage()
        sys.exit(0)
    else:
        usage()
