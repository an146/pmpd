import os, re
import sys
import urllib.request

class Wave:
    def play(self, player):
        pass

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
        print(self.playlist)

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


def read_waves_file(name, path):
    global aliases
    for line in open(path, 'r').readlines():
        line = line.strip()
        if line == "" or line.startswith('#'):
            continue

        m = re.match(r"(\w+): (.*)", line)
        if m == None:
            print("invalid wave desc:", line, file=sys.stderr)
        else:
            aliases[name + '/' + m.group(1)] = m.group(2)
            if m.group(1) == 'default':
                aliases[name] = m.group(2)
def read_waves():
    global aliases
    aliases = {}
    for dirname, dirnames, filenames in os.walk('waves/'):
        for filename in filenames:
            read_waves_file(filename, os.path.join(dirname, filename))
read_waves()


def create(desc = None, alias_depth = 10):
    if desc == None:
        return Wave()
    elif re.match('^[a-z]{1,4}://', desc) != None:
        return create_from_uri(desc)
    elif desc in aliases:
        if alias_depth <= 0:
            raise RuntimeError("too deep alias recursion: " + desc)
        return create(aliases[desc], alias_depth - 1)
    else:
        raise RuntimeError("file not found: " + desc)

def create_from_uri(uri):
    if uri.endswith(".pls"):
        return PlaylistWave(uri)
    else:
        return StreamWave(uri)
