import socket
import pickle
import threading
import tkinter as tk
import logging
import os
import sys
import datetime
from utils.file_interface import file_interface_utils
from robot_planner.scripts import planner_main

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

stm_config_file = \
    os.path.join(parent_dir, 'configs/stm_config.yaml')

robot_config_file = \
    os.path.join(os.path.dirname(parent_dir), 'configs/robot_config.yaml')

#stm_config = file_interface_utils.read_yaml_file(stm_config_file)
robot_config = file_interface_utils.read_yaml_file(robot_config_file)

class RobotSTM:
    def __init__(self):
        '''
            Class constuctor

            No need for socket communication, just make them different threads and use shared class variables
            with threading lock to avoid issues
        '''
        self.obstacle_list= []
        self.start_point = None
        self.goal_point = None

        # Set up the grid
        self.n, self.m = 15, 15  # Default values
        self.grid_size = 50  # Size of each square


    def launch_nodes(self):
        '''
            Create threads for processes
            1. UI thread (get user inputs and update parameters)
            2. Process monitor (spawns processes on triggers)
        '''
        user_interface_thread  = threading.Thread(target=self.user_interface)
        #process_monitor = threading.Thread(target=self.process_monitor)

        user_interface_thread.start()

        user_interface_thread.join()

    def user_interface(self):
        '''
            Receive user input and update parameters
            update display based on internal triggers
        '''

        # Set up the window and canvas
        self.window = tk.Tk()
        self.window.title("Interactive Grid")
        self.canvas = tk.Canvas(self.window, width=self.n*self.grid_size, height=self.m*self.grid_size, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)

        self.grid = [[0 for j in range(self.m)] for i in range(self.n)]  # Initialize grid to all 0s (white)

        # Create the squares on the canvas
        self.squares = []
        for i in range(self.n):
            self.row = []
            for j in range(self.m):
                x1, y1 = j*self.grid_size, i*self.grid_size
                x2, y2 = (j+1)*self.grid_size, (i+1)*self.grid_size
                self.square = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                self.row.append(self.square)
            self.squares.append(self.row)
        
        # Create a Text widget for displaying instructions
        self.instructions_text = tk.Text(self.window, height=5)
        self.instructions_text.pack(padx=10, pady=10)

        self.instructions_text.insert(tk.END, "Enter obstacles by clicking on the grid.\nClick 'Done adding obstacles' when finished.")

        # Bind mouse clicks to the canvas
        self.canvas.bind("<Button-1>", self.add_obstacle)
        self.canvas.bind("<Button-2>", self.select_start)
        self.canvas.bind("<Button-3>", self.select_goal)

        # Add a button to finish adding obstacles
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(side=tk.LEFT, padx=10)
        self.done_button = tk.Button(self.button_frame, text="Done adding obstacles", command=self.done_adding_obstacles)

        # Create two new buttons
        self.generate_path_button = tk.Button(self.button_frame, text="Generate Path", command=self.generate_path)
        self.clear_button = tk.Button(self.button_frame, text="Clear grid", command=self.clear_all)
        #self.retry_button = tk.Button(self.button_frame, text="Retry", command=self.)

        # Pack the three buttons into the button_frame widget
        self.done_button.pack(side=tk.TOP, padx=5)
        self.generate_path_button.pack(side=tk.TOP, padx=5)
        self.clear_button.pack(side=tk.TOP, padx=5)

        # Start the event loop
        self.window.mainloop()
    
    # Define functions for handling user input
    def add_obstacle(self, event):
        # Determine which square was clicked on
        x, y = event.x, event.y
        i, j = y//self.grid_size, x//self.grid_size
        self.obstacle_list.append([i, j])
        # Change the color of the square to black
        self.canvas.itemconfig(self.squares[i][j], fill="black")

    def select_start(self, event):
        # Clear the contents of the instructions_text widget
        self.instructions_text.delete(1.0, tk.END)
        self.instructions_text.insert(tk.END, "Enter goal position")

        # Determine which square was clicked on
        x, y = event.x, event.y
        i, j = y//self.grid_size, x//self.grid_size
        self.start_point = [i, j]
        # Change the color of the square to orange
        self.canvas.itemconfig(self.squares[i][j], fill="orange")
        # Unbind the mouse click from the canvas to prevent further editing
        self.canvas.unbind("<Button-1>")
        # Bind the mouse click to select goal node
        self.canvas.bind("<Button-1>", self.select_goal)
        # Prompt the user to select the goal node
        print("Select the goal node.")

    def select_goal(self, event):
        # Clear the contents of the instructions_text widget
        self.instructions_text.delete(1.0, tk.END)
        self.instructions_text.insert(tk.END, "Click 'generate path' to generate the path.\nClick 'clear all' to clear the grid")

        # Determine which square was clicked on
        x, y = event.x, event.y
        i, j = y//self.grid_size, x//self.grid_size
        self.goal_point = [i, j]
        # Change the color of the square to green
        self.canvas.itemconfig(self.squares[i][j], fill="green")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>")
        self.canvas.unbind("<Button-3>")

    def done_adding_obstacles(self):
        # Clear the contents of the instructions_text widget
        self.instructions_text.delete(1.0, tk.END)
        self.instructions_text.insert(tk.END, "Enter start position")

        # Unbind the mouse clicks from the canvas to prevent further editing
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>")
        self.canvas.unbind("<Button-3>")
        # Bind the mouse click to select start node
        self.canvas.bind("<Button-1>", self.select_start)
        # Prompt the user to select the start node
        print("Select the start node.")

    def generate_path(self):
        '''
            run this method to generate a path and update
            the grid
        '''
        self.instructions_text.delete(1.0, tk.END)
        self.instructions_text.insert(tk.END, "Generating .......")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>")
        self.canvas.unbind("<Button-3>")

        path, success_bool = planner_main.generate_path_2d(self.n, self.m, self.obstacle_list, self.start_point, self.goal_point)

        if success_bool:
            # Change the color of path squares to grey
            for p in path:
                self.canvas.itemconfig(self.squares[p[0]][p[1]], fill="grey")
            self.instructions_text.delete(1.0, tk.END)
            self.instructions_text.insert(tk.END, "Path found!")
            print("Path generated.")
        else:
            self.instructions_text.delete(1.0, tk.END)
            self.instructions_text.insert(tk.END, "Could not find a path")


    def clear_all(self):
        # Clear the contents of the instructions_text widget
        self.instructions_text.delete(1.0, tk.END)
        
        # Reset variable values
        self.obstacle_list= []
        self.start_point = None
        self.goal_point = None

        self.instructions_text.insert(tk.END, "Enter obstacles by clicking on the grid.\nClick 'Done adding obstacles' when finished.")

        # Change the color of all squares to white
        for i in range(self.n):
            for j in range(self.m):
                self.canvas.itemconfig(self.squares[i][j], fill="white")
        # Unbind all mouse clicks
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>")
        self.canvas.unbind("<Button-3>")
        # Rebind left click to add obstacles
        self.canvas.bind("<Button-1>", self.add_obstacle)
        # Prompt the user to start adding obstacles
        print("Add obstacles by clicking on the grid.")


    def input_callback(self):
        '''
            Listening callback
        '''
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Get the local machine name and port number
        self.host = socket.gethostname()
        
        # Obstacle port
        self.input_port = 12345

        # Bind the socket to a public host and port
        self.server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        self.server_socket.listen(1)

        while True:
            print("Waiting for a client connection...")
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} has been established.")

            # Receive data from the client
            data = client_socket.recv(1024)

            # Deserialize the data into an instance of MyClass
            obj = pickle.loads(data)

            # Print the data
            print(obj.data)

            # Close the client socket
            client_socket.close()

def stm_main():
    '''
        Main method to initialize the script
    '''
    # File name whre logs will be saved
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"robot_stm_log_{current_time}.log"
    log_target = os.path.join(os.path.dirname(parent_dir), "logs", file_name)
    fhandler = logging.FileHandler(filename=log_target, mode='w')
    
    # Setup the format of log messages
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    fhandler.setFormatter(formatter)
    
    # Create a logger
    stm_logger = logging.getLogger(__name__)
    stm_logger.setLevel(logging.INFO)
    stm_logger.addHandler(fhandler)

    # Logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    stm_logger.addHandler(console_handler)
    rst = RobotSTM()
    rst.launch_nodes()

if __name__ == '__main__':
    # Run the state machine
    stm_main()