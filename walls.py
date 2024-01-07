class Wall(Widget):
    def __init__(self, pos, size, **kwargs):
        super(Wall, self).__init__(**kwargs)
        self.pos = pos
        self.size = size