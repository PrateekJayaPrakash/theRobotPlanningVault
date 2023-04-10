from setuptools import find_packages, setup

setup(
    name='path_planning_vault',
    version='1.0.0',
    description='Trying to understand path planning',
    author='Prateek',
    author_email='keeparp.0@gmail.com',
    packages=find_packages(),
    package_data={'robot_planner':['configs/planner_config.yaml'], 'configs':['robot_config.yaml']},
)