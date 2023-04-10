import os
import sys
import datetime
import logging
from utils.file_interface import file_interface_utils
from robot_planner.include import node2d, graph2d

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

planner_config_file = \
    os.path.join(parent_dir, 'configs/planner_config.yaml')

robot_config_file = \
    os.path.join(os.path.dirname(parent_dir), 'configs/robot_config.yaml')

planner_config = file_interface_utils.read_yaml_file(planner_config_file)
robot_config = file_interface_utils.read_yaml_file(robot_config_file)


class Static2DPlanner:
    def __init__(self):
        pass
    
    def setup_obstacles(self):
        pass

    def initialize_graph(self):
        pass

def planner_main():
    '''

    '''
    # File name whre logs will be saved
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"log_{current_time}.log"
    log_target = os.path.join(os.path.dirname(parent_dir), "logs", file_name)
    fhandler = logging.FileHandler(filename=log_target, mode='w')
    
    # Setup the format of log messages
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    fhandler.setFormatter(formatter)
    
    # Create a logger
    planner_logger = logging.getLogger(__name__)
    planner_logger.setLevel(logging.INFO)
    planner_logger.addHandler(fhandler)

    # Logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    planner_logger.addHandler(console_handler)
    
    # Create an objec tof class planning
    s2d = Static2DPlanner()
    
if __name__ == '__main__':
    # Run main program
    planner_main()