
class Node2D:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.neighbors = []
        self.is_start_node = False
        self.is_goal_node = False
        self.is_obstacle = False
        self.parent_node = None