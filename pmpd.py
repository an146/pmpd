import getopt, os, sys
import socket
import logging as log
from gi.repository import GObject, Gtk
from config import config
from daemon import Daemon
from player import Player
import wave

GObject.threads_init()

def usage():
    print("usage: {0} start|stop|restart".format(sys.argv[0]))
    sys.exit(2)

def log_exceptions(ret):
    def do_log_exceptions(f):
        def new_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                log.error('<<<Traceback>>>', exc_info=True)
                return ret
        return new_f
    return do_log_exceptions

class Pmpd(Daemon):
    def __init__(self):
        self.cmdin = []
        self.wavedesc = None
        super().__init__(pidfile = config.pidfile)

    @log_exceptions(True)
    def run(self, background):
        loglevel = log.INFO
        if background:
            f = open(config.logfile, 'a', 1)
            log.basicConfig(filename=config.logfile, level=loglevel)
            self.close_stdfiles()
            self.listen_to_port()
        else:
            log.basicConfig(stream=sys.stderr, level=loglevel)
            self.listen_to_file(sys.stdin)

        self.player = Player()
        self.wave = wave.create(self.wavedesc)
        self.wave.play(self.player)
        self.mainloop = GObject.MainLoop()
        context = self.mainloop.get_context()
        self.mainloop.run()
        return
        while True:
            try:
                context.iteration(True)
            except:
                log.error('Traceback', exc_info=True)

    def run_wave(self, wavedesc):
        self.wavedesc = wavedesc
        self.run_in_foreground()

    def listen_to_port(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((config.host, config.port))
        self.socket.setblocking(0)
        self.socket.listen(5)
        conds = GObject.IO_IN | GObject.IO_ERR | GObject.IO_HUP
        GObject.io_add_watch(self.socket, conds, self.socket_callback)

    def listen_to_file(self, f):
        self.cmdin += [f]
        conds = GObject.IO_IN | GObject.IO_ERR | GObject.IO_HUP
        GObject.io_add_watch(f, conds, self.cmdin_callback)

    @log_exceptions(True)
    def socket_callback(self, socket, cond):
        assert socket == self.socket
        if cond == GObject.IO_IN:
            (clientsocket, address) = socket.accept()
            log.info('connected: %s', address)
            self.listen_to_file(clientsocket.makefile('r', 1))
        else:
            log.info('cmdin_callback: %s %s', cmdin, cond)
        return True

    @log_exceptions(True)
    def cmdin_callback(self, cmdin, cond):
        if cond & GObject.IO_IN:
            while True:
                l = cmdin.readline()
                if l == '':
                    break
                l = l.strip()
                log.info('cmd: %s', l)
            cond &= ~GObject.IO_IN
        if cond & GObject.IO_HUP:
            log.info('cmdin_hup: %s', cmdin)
            self.cmdin.remove(cmdin)
            return False
        if cond:
            log.info('cmdin_callback: %s %s', cmdin, cond)
        return True

def main():
    configfile = None
    opts, args = getopt.getopt(sys.argv[1:], 'C:')
    for opt, val in opts:
        if opt == 'C':
            configfile = val
    config.read(configfile)
    wave.check_wavesdir()

    if args == []:
        action = lambda: Pmpd().run_in_foreground()
    elif args == ['start']:
        action = lambda: Pmpd().start()
    elif args == ['stop']:
        action = lambda: Pmpd().stop()
    elif args == ['restart']:
        action = lambda: Pmpd().restart()
    elif args[0] == 'run':
        action = lambda: Pmpd().run_wave(args[1])
    else:
        print("unknown command:", args[0], file=sys.stderr)
        usage()

    action()
    return 0

if __name__ == "__main__":
    sys.exit(main())
