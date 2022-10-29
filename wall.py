class Wall():
    # this one is more of a trick to have the walls as sprites without actually loading anything
    def __init__(self, x, y, width, height, description):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description


    def get_width(self):
        return self.width

    def get_height(self):
        return self.height