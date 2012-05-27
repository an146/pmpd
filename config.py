import os, os.path
import sys
from configparser import ConfigParser

conf = ConfigParser()

class config():
    @classmethod
    def read(cls, configfile=None):
        if configfile != None:
            cls.configfile = configfile
        elif os.path.isdir(os.environ['HOME']):
            cls.localdir = os.path.expandvars("$HOME/.pmpd")
            if not os.path.isdir(cls.localdir):
                os.mkdir(cls.localdir)
            cls.configfile = os.path.join(cls.localdir, "pmpd.conf")
            if not os.path.isfile(cls.configfile):
                cls.generate_config()
        else:
            cls.configfile = "/etc/pmpd.conf"

        if conf.read(cls.configfile) != [cls.configfile]:
            raise RuntimeError("couldn't read config")
        print("using config:", cls.configfile, file=sys.stderr)
        cls.wavesdir = conf.get('pmpd', 'wavesdir')
        cls.pidfile = conf.get('pmpd', 'pidfile')
        cls.logfile = conf.get('pmpd', 'logfile')

    @classmethod
    def generate_config(cls):
        c = open(cls.configfile, 'w')
        conf['pmpd'] = {'wavesdir': os.path.join(cls.localdir, 'waves/'),
                        'pidfile': '/tmp/pmpd.pid',
                        'logfile': '/tmp/pmpd.log'}
        conf.write(c)
        c.close()
        print("created config:", cls.configfile, file=sys.stderr)
