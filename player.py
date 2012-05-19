import sys
import urllib.request
from gi.repository import Gst

class Player:
    def __init__(self):
        Gst.init(None)

        self.pipeline = Gst.Pipeline()
        self.playbin = None

        self.bus = self.pipeline.get_bus()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::tag', self.on_tag)
        self.bus.connect('message::error', self.on_error)
        self.bus.connect('message::buffering', self.on_buffering)
        #self.bus.connect('message', self.on_message)
        self.bus.add_signal_watch()

    def play(self, uri):
        self.stop()
        print("playing {0}".format(uri), file=sys.stderr)
        self.playbin = Gst.ElementFactory.make("playbin2", None)
        self.playbin.set_property('uri', uri)
        self.pipeline.add(self.playbin)
        self.pipeline.set_state(Gst.State.PLAYING)

    def play_pls(self, uri):
        req = urllib.request.urlopen(uri)
        assert req.headers['Content-Type'].find('audio/x-scpls') == 0
        print(req.read().decode('utf-8'))

    def stop(self):
        if self.playbin:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.pipeline.remove(self.playbin)
        self.playbin = None

    def on_eos(self, bus, msg):
        print('on_eos', file=sys.stderr)
        self.pipeline.set_state(Gst.State.NULL)
        #self.mainloop.quit()

    def on_tag(self, bus, msg):
        taglist = msg.parse_tag()
        print('on_tag:', file=sys.stderr)
        for key in taglist.keys():
            print("{0} = {1}".format(key, taglist[key]), file=sys.stderr)

    def on_error(self, bus, msg):
        error = msg.parse_error()
        print('on_error:', error[1], file=sys.stderr)
        #self.mainloop.quit()

    def on_buffering(self, bus, msg):
        buffering = msg.parse_buffering()
        print('on_buffering: {0}'.format(buffering), file=sys.stderr)

    def on_message(self, bus, msg):
        print('message: {0}'.format(type(msg)), file=sys.stderr)
