import getopt, sys
from gi.repository import GObject, Gtk
from config import config
from daemon import Daemon
from player import Player
import wave

GObject.threads_init()

def usage():
    print("usage: {0} start|stop|restart".format(sys.argv[0]))
    sys.exit(2)

class Pmpd(Daemon):
    def __init__(self):
        self.wave = wave.create()
        super().__init__(pidfile = config.pidfile, logfile = config.logfile)

    def run(self):
        self.player = Player()
        self.wave.play(self.player)
        self.mainloop = GObject.MainLoop()
        self.mainloop.run()
        print("mainloop ended", file=sys.stderr)

def main():
    configfile = None
    opts, args = getopt.getopt(sys.argv[1:], 'C:')
    for opt, val in opts:
        if opt == 'C':
            configfile = val
    config.read(configfile)
    wave.check_wavesdir()

    daemon = Pmpd()
    if len(sys.argv) == 1:
        daemon.run()
    else:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'run' == sys.argv[1]:
            daemon.wave = wave.create(*sys.argv[2:])
            daemon.run()
        else:
            print(sys.argv[1])
            usage()
        sys.exit(0)

if __name__ == "__main__":
    main()
