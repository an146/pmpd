import re
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


def create(desc = None):
    if desc == None:
        return Wave()
    elif re.match('^[a-z]{1,4}://', desc) != None:
        return create_from_uri(desc)
    else:
        raise RuntimeError("file not found: " + desc)

def create_from_uri(uri):
    if uri.endswith(".pls"):
        return PlaylistWave(uri)
    else:
        return StreamWave(uri)
