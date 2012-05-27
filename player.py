import sys
import logging as log
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
        log.info("playing %s", uri)
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
            log.info('error: %s', msg.parse_error())
        elif t == 'stream_status':
            status, src = msg.parse_stream_status()
            log.info('stream_status: %16s %s', src.name, status.value_nick)
        elif t == 'state_changed':
            st = list(map(lambda x: x.value_nick, msg.parse_state_changed()))
            if msg.src == self.pipeline:
                log.info('pipeline_state_changed: %s', st)
            else:
                log.debug('state_changed: %16s %s', msg.src.name, st)
        elif t == 'element':
            log.info('element: %16s <%s>', msg.src.name, msg.get_structure().get_name())
        elif t == 'tag':
            log.info('tag: %s', msg.parse_tag().to_string())
        elif t == 'buffering':
            log.debug('buffering: %s', msg.parse_buffering())
        else:
            log.info('message: %s', t)
