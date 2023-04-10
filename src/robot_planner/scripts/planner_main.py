import os
from utils.file_interface import file_interface_utils

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

planner_config_file = \
    os.path.join(parent_dir, 'configs/planner_config.yaml')

robot_config_file = \
    os.path.join(os.path.dirname(parent_dir), 'configs/robot_config.yaml')

planner_config = file_interface_utils.read_yaml_file(planner_config_file)
robot_config = file_interface_utils.read_yaml_file(robot_config_file)


def planner_main():
    pass

if __name__ == '__main__':
    planner_main()