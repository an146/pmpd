import logging as log
import os, re
import sys
import urllib.request
from config import config

class Wave:
    def play(self, player):
        raise RuntimeError("Wave.play")

class StreamWave(Wave):
    def __init__(self, uri):
        self.uri = uri

    def play(self, player):
        player.play_uri(self.uri)

class PlaylistWave(Wave):
    def __init__(self, uri):
        req = urllib.request.urlopen(uri)
        assert req.headers['Content-Type'].find('audio/x-scpls') == 0
        self.playlist = req.read().decode('utf-8')
        log.debug("Got playlist:\n" + self.playlist)

    def play(self, player):
        for l in self.playlist.splitlines():
            if l[0:4] == "File":
                break
        else:
            l = ""

        if l == "":
            raise RuntimeError("no streams in playlist")
        else:
            player.play_uri(l[l.find("=")+1:])


def create(desc = None, alias_depth = 3):
    if desc == None:
        return Wave()
    desc = desc.strip()
    if re.match('^[a-z]{1,4}://', desc) != None:
        return create_from_uri(desc)

    # check aliases
    desc1 = expand_alias(desc)
    if desc1 == None:
        raise RuntimeError("file not found: " + desc)
    if alias_depth <= 0:
        raise RuntimeError("too deep alias recursion: " + desc)
    return create(desc1, alias_depth - 1)

def expand_alias(alias):
    try:
        for l in open(os.path.join(config.wavesdir, alias)).readlines():
            l = l.strip()
            if not l.startswith('#'):
                return l
    except(IOError): pass
    return None

def create_from_uri(uri):
    if uri.endswith(".pls"):
        return PlaylistWave(uri)
    else:
        return StreamWave(uri)

def check_wavesdir():
    if not os.path.isdir(config.wavesdir):
        os.mkdir(config.wavesdir)
        open(os.path.join(config.wavesdir, 'rad'), 'w').write(
            "http://195.151.189.25/RAD.mp3")
        log.info("created", config.wavesdir)
