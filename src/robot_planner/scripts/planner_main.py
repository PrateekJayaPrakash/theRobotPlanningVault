import os
import sys
import datetime
import logging
import heapq
from utils.file_interface import file_interface_utils
from robot_planner.include import node2d, graph2d

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

planner_config_file = \
    os.path.join(parent_dir, 'configs/planner_config.yaml')

robot_config_file = \
    os.path.join(os.path.dirname(parent_dir), 'configs/robot_config.yaml')

planner_config = file_interface_utils.read_yaml_file(planner_config_file)
robot_config = file_interface_utils.read_yaml_file(robot_config_file)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Static2DPlanner:
    def __init__(self, grid_width, grid_height, obstacles, start, goal):
        '''
            Class constructor
        '''
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.obstacle_coordinate_list = obstacles
        self.start_point = start
        self.goal_point = goal
        self.goal_found = False
        self.graph2D = graph2d.Graph2D(self.grid_width, self.grid_height)
        self.node_queue = PriorityQueue()
        self.initialize_graph()
        self.setup_obstacles()
        self.a_star_algo()
        #self.print_path()
    
    def print_path(self):
        n = self.graph2D.nodes[self.goal_point[0]][self.goal_point[1]]
        print(n.x, n.y)
        while n.parent_node is not None:
            n = n.parent_node
            print(n.x, n.y)

    def robot_path(self):
        n = self.graph2D.nodes[self.goal_point[0]][self.goal_point[1]]
        return_list = []
        while n.parent_node is not None and not n.is_start_node:
            n = n.parent_node
            return_list.append([n.x, n.y])

        return return_list, self.goal_found

    def a_star_algo(self):
        start_node = self.graph2D.nodes[self.start_point[0]][self.start_point[1]]
        goal_node = self.graph2D.nodes[self.goal_point[0]][self.goal_point[1]]
        start_node.cost = 0
        self.node_queue.put(self.get_cost(start_node, goal_node), start_node)
        
        while not self.node_queue.is_empty():
            current = self.node_queue.get()
            current.visited = True
            for n in self.get_neighbors(current):
                if (not n.is_obstacle) and not n.visited:
                    if current.cost + self.get_cost(current, n) < n.cost:
                        n.cost = current.cost + self.get_cost(current, n)
                        n.parent_node = current

                    self.node_queue.put(n.cost + self.get_cost(n, goal_node), n)

                if n.is_goal_node:
                    self.goal_found = True
                    print("goal found")
                    return

    def get_neighbors(self, node1):
        neighbors = []
        if node1.x < self.grid_width - 1:
            neighbors.append(self.graph2D.nodes[node1.x +1][node1.y])
        if node1.x > 0:
            neighbors.append(self.graph2D.nodes[node1.x - 1][node1.y])
        if node1.y < self.grid_height - 1:
            neighbors.append(self.graph2D.nodes[node1.x][node1.y + 1])
        if node1.y > 0:
            neighbors.append(self.graph2D.nodes[node1.x][node1.y - 1])
        return neighbors

    def get_cost(self, node1, node2):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def setup_obstacles(self):
        for obs in self.obstacle_coordinate_list:
            self.graph2D.nodes[obs[0]][obs[1]].is_obstacle = True

    def initialize_graph(self):
        '''
            Initialize the graph by creating nodes
        '''
        self.graph2D.width = self.grid_width
        self.graph2D.height = self.grid_height

        for i in range(0, self.grid_width):
            for j in range(0, self.grid_height):
                self.graph2D.nodes[i][j] = node2d.Node2D(i,j)
        
        self.graph2D.nodes[self.goal_point[0]][self.goal_point[1]].is_goal_node = True
        self.graph2D.nodes[self.start_point[0]][self.start_point[1]].is_start_node = True

def generate_path_2d(grid_width, grid_height, obstacles, start, goal):
    '''
        Callable method to generate a path between
        start and goal
    '''
    # File name whre logs will be saved
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"log_{current_time}.log"
    log_target = os.path.join(os.path.dirname(parent_dir), "logs", file_name)
    #fhandler = logging.FileHandler(filename=log_target, mode='w')
    
    # Setup the format of log messages
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    #fhandler.setFormatter(formatter)
    
    # Create a logger
    planner_logger = logging.getLogger(__name__)
    planner_logger.setLevel(logging.INFO)
    #planner_logger.addHandler(fhandler)

    # Logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    planner_logger.addHandler(console_handler)
    
    # Create an objec tof class planning
    s2d = Static2DPlanner(grid_width, grid_height, obstacles, start, goal)

    return s2d.robot_path()
    
if __name__ == '__main__':
    # Run main program
    generate_path_2d(10, 5, [[2, 2]], [0, 0], [5, 4])