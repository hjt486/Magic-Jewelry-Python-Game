import subprocess
import time
import random

class grid:
    def __init__(self):
        # Define empty hole char, and create 6 x 13 grid
        self.hole = '-'
        self.grid = [[self.hole] * 6 for i in range(14)]
        #self.color = ['b', 'r', 'y', 'g', 'p', 'o']
        # Define available colors
        self.color = ['✤', '✹', '✿', '♣', '♦', '♥']
        # 3 in 1 bar and its position
        self.bar = []
        self.bar_position = []
    
    # Generate existed bottom for fun (or more for testing purpose)
    def generateBottomGrid(self, height, ladder = False):
        for j in range(len(self.grid) - height, len(self.grid)):
            for i in range(len(self.grid[0])):
                self.grid[j][i] = self.color[random.randrange(0, 6)]
        # If ladder is True, generate ladder shape
        # (you can test to see difference)
        if ladder == True:
            x = 0
            for j in range(len(self.grid)-2, len(self.grid)-1-height-1, -1):
                x += 1
                for i in range(len(self.grid[0])-1, len(self.grid[0])-1-x, -1):
                    self.grid[j][i] = self.hole
    
    # Generate a random combiantion of 3 in 1 bar
    def generateBar(self):
        # Clear the previous bar
        self.bar.clear()
        self.bar_position.clear()
        # Default position i at [(3, 0),(3, 1),(3, 2)]
        for i in range(3):
            # Generate random number from self.color for a bar at original position
            point = self.color[random.randrange(0, 6)]
            self.bar.append(point)
            self.grid[i][3] = point
            self.bar_position = [(3, 0),(3, 1),(3, 2)]
    
    # Move bar around the grid
    def moveBar(self, direction) -> bool:
        # Define the x y coordinates change per step
        direction_list = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        # a and b is the next direction step
        a, b = direction_list[direction][0], direction_list[direction][1]
        # Get x, y coordinates for each element of the bar (total 3)
        # This is kinda redundant, may improve in the future 
        element1x, element1y = self.bar_position[0][0], self.bar_position[0][1]
        element2x, element2y = self.bar_position[1][0], self.bar_position[1][1]
        element3x, element3y = self.bar_position[2][0], self.bar_position[2][1]
        # Get width and height
        width = len(self.grid[0])
        height = len(self.grid)
        # When reach left right, up down edges, return False to trigger Move Failed
        if element1x + a < 0 or element1x + a > width - 1 or element1y + b < 0 or element3y + b > height - 1:
            return False
        # To Detect surrounding points if occupied by existed points
        if direction == 'left' or direction == 'right':
            if self.grid[element1y][element1x+a] != self.hole or self.grid[element2y][element2x+a] != self.hole or self.grid[element3y][element3x+a] != self.hole:
                return False
        if direction == 'up' and self.grid[element1y - 1][element1x] != self.hole or direction == 'down' and self.grid[element3y + 1][element1x] != self.hole:
            return False
        # This is to prevent fake shadow value, for down movement, switch value from bottom.
        if direction == 'up' or direction =='left' or direction == 'right':
            start = 0
            end = 3
            step = 1
        elif direction == 'down':
            start = 2
            end = -1
            step = -1
        # Move by switch value of each point
        for k in range(start, end, step):
            i, j = self.bar_position[k]
            print(a, b)
            self.grid[j][i], self.grid[j+b][i+a] = self.grid[j+b][i+a], self.grid[j][i]
            self.bar_position[k] = (i+a, j+b)
        # Return True for successful move operations
        return True
    
    # Rotate the bar in single direction (up to down)
    def rotateBar(self):
        self.bar[0], self.bar[1], self.bar[2] = self.bar[2], self.bar[0], self.bar[1]
        # Update the grid value after rotation, may be redundant, will change in the future
        for k, (x, y) in enumerate(self.bar_position):
            self.grid[y][x] = self.bar[k]

    # To drop the bar (fix the bar on the grid), and get a new bar
    def dropBar(self):
        for i in range(3):
            # Call apply function to do removing check
            self.applyFromPoint(self.bar_position[i][0], self.bar_position[i][1])
        self.generateBar()

    # A text version of display
    def displayGrid(self):
        print("==========Magic Jewelry==========")
        print("      (Alpha) By Jiatai Han      ")
        print("Press Arrow Key and Enter to move bar")
        print("Press '/' and Enter to rotate bar")
        print("Press Enter to drop the Bar")
        print("Press Esc and Enter to quit")
        print("")
        print("     0    1    2    3    4    5")
        for i, row in enumerate(self.grid):
            print(str(i).zfill(2), row)
        print("")
    
    # Apply the removing check from a point in chain reaction
    def applyFromPoint(self, x, y):
        # Create a set to prevent recorde duplicate points
        points_to_be_removed = set()
        directions = ['left', 'right', 'up', 'down', 'upleft', 'upright', 'downleft', 'downright']
        # check all directions
        for direction in directions:
            # Call chain reaction to get the sets of points that needs to be removed
            points_to_be_removed |= self.findChain(x,y, direction)
        # After get all points, remove them
        for i, j in points_to_be_removed:
            self.grid[j][i] = self.hole
    
    # Chain reaction method, find a chain(same color) in a direction
    def findChain(self, x, y, direction):
        # Define the change of x, y in each step
        direction_pointer = {
            'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1),
            'upleft': (-1, -1), 'upright': (1, -1), 'downleft': (-1, 1), 'downright': (1, 1)}
        a, b = direction_pointer[direction]
        # A set to contains points that need to be removed
        chain = {(x,y)}
        i, j = x, y
        # A counter to count how many same color points
        counter = 0
        # Stop when reach edges or two points share different colors
        # Else continue adding the same color points' coordinates to the set
        while i != -1 and j != -1 and i != len(self.grid[0]) and j != len(self.grid) and self.grid[j][i] == self.grid[y][x]:
            chain.add((i, j))
            counter += 1
            i += a
            j += b
        # Return the set only if more than 3 same color points in a chain, else return empty set
        if counter >= 3:
            return chain
        else:
            return set()
        
def main():
    directions = {"\x1b[A" : 'up', "\x1b[B" : 'down', "\x1b[D" : 'left', "\x1b[C" : 'right'}
    newGame = grid()
    newGame.generateBottomGrid(3, True)
    newGame.generateBar()
    while True:
        # Refresh screen
        subprocess.call("clear")
        newGame.displayGrid()
        user_input = input("Give a command\n")
        #print(directions[user_input])
        if user_input == '':
            newGame.dropBar()
        elif user_input == '/':
            newGame.rotateBar()
        elif user_input == '\x1b':
            return
        else:
            try:
                if not newGame.moveBar(directions[user_input]):
                    print("Move Failed!")
                    time.sleep(1)
            except:
                print("Wrong Key!")
                time.sleep(1)

if __name__ == "__main__":
    main()