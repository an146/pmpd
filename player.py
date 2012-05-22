import sys
from gi.repository import Gst

class Player:
    def __init__(self):
        Gst.init(None)

        self.pipeline = Gst.Pipeline()
        self.playbin = None

        self.bus = self.pipeline.get_bus()
        self.bus.connect('message', self.on_message)
        self.bus.add_signal_watch()

    def play_uri(self, uri):
        self.stop()
        print("playing", uri, file=sys.stderr)
        self.playbin = Gst.ElementFactory.make("playbin", None)
        self.playbin.set_property('uri', uri)
        self.pipeline.add(self.playbin)
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        if self.playbin:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.pipeline.remove(self.playbin)
        self.playbin = None

    def on_message(self, bus, msg):
        t = msg.type.first_value_nick
        if t == 'error':
            print('error:', msg.parse_error(), file=sys.stderr)
        elif t == 'stream_status':
            print('stream_status:', msg.parse_stream_status(), file=sys.stderr)
        elif t == 'state_changed':
            st = list(map(lambda x: x.value_nick, msg.parse_state_changed()))
            print('state_changed:', msg.src, st, file=sys.stderr)
        elif t == 'element':
            print('element:', msg.get_structure(), file=sys.stderr)
        elif t == 'tag':
            print('tag:', msg.parse_tag().to_string(), file=sys.stderr)
        elif t == 'buffering':
            print('buffering:', msg.parse_buffering(), file=sys.stderr)
        else:
            print('message:', t, file=sys.stderr)
