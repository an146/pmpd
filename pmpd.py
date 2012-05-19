import sys, time
from daemon import Daemon
from player import Player
from gi.repository import GObject, Gtk

GObject.threads_init()

def usage():
    print("usage: {0} start|stop|restart".format(sys.argv[0]))
    sys.exit(2)

class PmpdDaemon(Daemon):
    def __init__(self):
        super().__init__(pidfile = '/tmp/pmpd.pid', logfile = '/tmp/pmpd.log')

    def run(self):
        self.player = Player()
        self.player.play('http://u16b.di.fm:80/di_ambient')
        self.mainloop = GObject.MainLoop()
        self.mainloop.run()
        print("mainloop ended", file=sys.stderr)

if __name__ == "__main__":
    daemon = PmpdDaemon()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'run' == sys.argv[1]:
            daemon.run()
        else:
            usage()
        sys.exit(0)
    else:
        usage()
