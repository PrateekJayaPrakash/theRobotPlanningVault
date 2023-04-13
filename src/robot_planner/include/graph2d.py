from collections import defaultdict

class Graph2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = [[None for j in range(height)] for i in range(width)]