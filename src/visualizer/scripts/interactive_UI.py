import tkinter as tk

# Set up the grid
n, m = 15, 15  # Default values
grid_size = 50  # Size of each square

# Set up the window and canvas
window = tk.Tk()
window.title("Interactive Grid")
canvas = tk.Canvas(window, width=n*grid_size, height=m*grid_size, borderwidth=0, highlightthickness=0)
canvas.pack(side=tk.LEFT)

grid = [[0 for j in range(m)] for i in range(n)]  # Initialize grid to all 0s (white)

# Create the squares on the canvas
squares = []
for i in range(n):
    row = []
    for j in range(m):
        x1, y1 = j*grid_size, i*grid_size
        x2, y2 = (j+1)*grid_size, (i+1)*grid_size
        square = canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        row.append(square)
    squares.append(row)

# Define functions for handling user input
def add_obstacle(event):
    # Determine which square was clicked on
    x, y = event.x, event.y
    i, j = y//grid_size, x//grid_size
    # Change the color of the square to black
    canvas.itemconfig(squares[i][j], fill="black")

def select_start(event):
    # Clear the contents of the instructions_text widget
    instructions_text.delete(1.0, tk.END)
    instructions_text.insert(tk.END, "Enter goal position")

    # Determine which square was clicked on
    x, y = event.x, event.y
    i, j = y//grid_size, x//grid_size
    # Change the color of the square to orange
    canvas.itemconfig(squares[i][j], fill="orange")
    # Unbind the mouse click from the canvas to prevent further editing
    canvas.unbind("<Button-1>")
    # Bind the mouse click to select goal node
    canvas.bind("<Button-1>", select_goal)
    # Prompt the user to select the goal node
    print("Select the goal node.")

def select_goal(event):
    # Clear the contents of the instructions_text widget
    instructions_text.delete(1.0, tk.END)
    instructions_text.insert(tk.END, "Click 'generate path' to generate the path.\nClick 'clear all' to clear the grid")

    # Determine which square was clicked on
    x, y = event.x, event.y
    i, j = y//grid_size, x//grid_size
    # Change the color of the square to green
    canvas.itemconfig(squares[i][j], fill="green")

def done_adding_obstacles():
    # Clear the contents of the instructions_text widget
    instructions_text.delete(1.0, tk.END)
    instructions_text.insert(tk.END, "Enter start position")

    # Unbind the mouse clicks from the canvas to prevent further editing
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-2>")
    canvas.unbind("<Button-3>")
    # Bind the mouse click to select start node
    canvas.bind("<Button-1>", select_start)
    # Prompt the user to select the start node
    print("Select the start node.")

def generate_path():
    # TODO: Add path generation logic
    print("Path generated.")

def clear_all():
    # Clear the contents of the instructions_text widget
    instructions_text.delete(1.0, tk.END)
    instructions_text.insert(tk.END, "Enter obstacles by clicking on the grid.\nClick 'Done adding obstacles' when finished.")

    # Change the color of all squares to white
    for i in range(n):
        for j in range(m):
            canvas.itemconfig(squares[i][j], fill="white")
    # Unbind all mouse clicks
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-2>")
    canvas.unbind("<Button-3>")
    # Rebind left click to add obstacles
    canvas.bind("<Button-1>", add_obstacle)
    # Prompt the user to start adding obstacles
    print("Add obstacles by clicking on the grid.")

# Create a Text widget for displaying instructions
instructions_text = tk.Text(window, height=5)
instructions_text.pack(padx=10, pady=10)

instructions_text.insert(tk.END, "Enter obstacles by clicking on the grid.\nClick 'Done adding obstacles' when finished.")

# Bind mouse clicks to the canvas
canvas.bind("<Button-1>", add_obstacle)
canvas.bind("<Button-2>", select_start)
canvas.bind("<Button-3>", select_goal)

# Add a button to finish adding obstacles
button_frame = tk.Frame(window)
button_frame.pack(side=tk.LEFT, padx=10)
done_button = tk.Button(button_frame, text="Done adding obstacles", command=done_adding_obstacles)

# Create two new buttons
generate_path_button = tk.Button(button_frame, text="Generate Path", command=generate_path)
clear_button = tk.Button(button_frame, text="Clear grid", command=clear_all)

# Pack the three buttons into the button_frame widget
done_button.pack(side=tk.TOP, padx=5)
generate_path_button.pack(side=tk.TOP, padx=5)
clear_button.pack(side=tk.TOP, padx=5)

# Start the event loop
window.mainloop()
