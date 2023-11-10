
class Node2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.cost = float('inf')
        self.visited = False
        self.is_start_node = False
        self.is_goal_node = False
        self.is_obstacle = False
        self.parent_node = None
    
    def __lt__(self, other):
        if self.cost <= other.cost:
            return True
        else:
            return False