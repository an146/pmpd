class Wave:
    def __init__(self, desc = None):
        self.desc = desc

    def play(self, player):
        if self.desc != None:
            player.play(self.desc)
