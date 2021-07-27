import sys

# Node class has been created with a function containing the node attributes.

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# StackFrontier Class has been created to handle the node operations such as Add, remove,delete and to contain.

class StackFrontier():

# Creates a set to hold the frontier nodes.    
    def __init__(self):
        self.frontier = []
# Adds nodes to the frontier set.
    def add(self,node):
        self.frontier.append(node)
# Contains the states of each of the nodes in frontier.
    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)
# Clears the nodes from the frontier.
    def empty(self):
        return len(self.frontier) == 0
# removes the nodes that are explored and eliminated
    def remove(self):
# Checks if the frontier is blanks and raise exception 
        if self.empty():
            raise Exception("Empty frontier.")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

#QueueFrontier class has been created to demonstrate the differnce between the Depth first search and Breadth first search as the queue frontier is used to depict the Breadth first search (BFS)

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Enpty Frontier")
        else:
# In contrast to StackFrontier the first value that got in has been eliminated in Queue Frontier
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
#class maze has been created to first the maze from a txt file and validate before explored
class Maze():
# __init__ function reads the file
    def  __init__(self,filename):
        with open(filename) as f:
            contents = f.read()
#validates the Start and Goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one starting point.")
        if contents.count("B") != 1:
            raise Exception("Maze must have excatly one goal")
#Determine height and width of the input maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
#Keep track of walls
        self.walls = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
#A function to print the maze
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i,j) == self.start:
                    print("A", end="")
                elif (i,j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
#A function to check on the neighors.
    def neighbors(self,state):
        row, col = state
        candidates = [
            ("up", (row -1 , col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
# The result set collects the action and coordinates of other neighbors
        result = []
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action , (r, c)))
        return result
# Solve function finds a solution to maze, if one exists.    
    def solve(self):
#Keep track of the number of states explored
        self.num_explored = 0
#Inititalize frontier to just the starting function
        start = Node(state=self.start, parent = None , action = None)
        frontier = StackFrontier()
        frontier.add(start)
#Initialize an empty explored set
        self.explored=set()
#Looping until a soultion is found
        while True:
             #If nothing left in frontier ,then no path
            if frontier.empty():
                 raise Exception("No selection")
# Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
# If node is the goal, then we have a solution
            if node.state == self.goal:
                actions =[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node= node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
# Mark node as explored
            self.explored.add(node.state)
# Add neighbors to the frontier
            for action,state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state= state,parent = node, action = action)
                    frontier.add(child)
    def output_image(self,filename,show_solution=True,show_explored = False ):
        from PIL import Image,ImageDraw
        cell_size = 50
        cell_border = 2 
# Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size,self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                # Walls
                if col:
                    fill = (40,40,40)
                # Start
                elif (i,j) == self.start:
                    fill = (255,0,0)
                # Goal
                elif (i,j) == self.goal:
                    fill = (0,171,28)
                # Solution
                elif solution is not None and show_solution and (i,j) in solution:
                    fill = (220,235,113)
                # Explored
                elif solution is not None and show_explored and (i,j) in self.explored:
                    fill = (212,97,85)
                # Empty Cell
                else:
                    fill = (237,240,252)
                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
        img.save(filename)
if len(sys.argv) != 2:
    sys.exit("Usage : Python maze.py maze.txt")
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States explored :" , m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored = True)