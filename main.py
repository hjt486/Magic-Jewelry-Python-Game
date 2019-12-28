import subprocess
import time
import random
from pynput import keyboard

class grid:
    def __init__(self):
        # Define empty hole char, and create 6 x 13 grid
        self.hole = '-'
        self.grid = [[self.hole] * 6 for i in range(16)]
        self.grid_width = len(self.grid[0])
        self.grid_height = len(self.grid)
        #self.color = ['b', 'r', 'y', 'g', 'p', 'o']
        # Define available colors
        self.color = ['✤', '✹', '✿', '♣', '♦', '♥']
        # 3 in 1 bar and its position
        self.bar_next = []
        self.bar_next_position = []
        self.bar = []
        self.bar_position = []
        self.speed = 1
    
    # Generate existed bottom for fun (or more for testing purpose)
    def generateBottomGrid(self, height, ladder = False):
        for j in range(self.grid_height - height, self.grid_height):
            for i in range(self.grid_width):
                self.grid[j][i] = self.color[random.randrange(0, 6)]
        # If ladder is True, generate ladder shape
        # (you can test to see difference)
        if ladder == True:
            x = 0
            for j in range(self.grid_height-2, self.grid_height-1-height-1, -1):
                x += 1
                for i in range(self.grid_width-1, self.grid_width-1-x, -1):
                    self.grid[j][i] = self.hole
    
    # Generate a random combiantion of 3 in 1 bar
    def generateARandomBar(self):
        # Generate random number from self.color for a bar at original position
        return [self.color[random.randrange(0, 6)] for i in range(3)], [(3, 0),(3, 1),(3, 2)]
        
    def generateBars(self):
        if not self.bar_next:
            self.bar, self.bar_position = self.generateARandomBar()
            self.bar_next, self.bar_next_position = self.generateARandomBar()
        else:
            self.bar, self.bar_position = self.bar_next, self.bar_next_position
            self.bar_next, self.bar_next_position = self.generateARandomBar()
        for i in range(3):
            x, y = self.bar_position[i][0], self.bar_position[i][1]
            self.grid[y][x] = self.bar[i]

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
        width = self.grid_width
        height = self.grid_height
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
            #print(a, b)
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
        bar_bottom_x, bar_bottom_y = self.bar_position[2][0], self.bar_position[2][1]
        while bar_bottom_y + 1 < self.grid_height and self.grid[bar_bottom_y + 1][bar_bottom_x] == self.hole:
            self.moveBar("down")
            bar_bottom_x, bar_bottom_y = self.bar_position[2][0], self.bar_position[2][1]
        for i in range(3):
            # Call apply function to do removing check
            self.applyFromPoint(self.bar_position[i][0], self.bar_position[i][1])
        self.gravityAllPoints()
        self.generateBars()
    
    def gravityDrop(self):
        bar_bottom_x, bar_bottom_y = self.bar_position[2][0], self.bar_position[2][1]
        if bar_bottom_y + 1 < self.grid_height and self.grid[bar_bottom_y + 1][bar_bottom_x] == self.hole:
            self.moveBar("down")
            #print(self.grid[bar_bottom_y + 1][bar_bottom_x])
            #print(bar_bottom_x, bar_bottom_y + 1)
        else:
            #print("test")
            self.dropBar()
        time.sleep(self.speed)

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
        for i in range(3, len(self.grid)):
            print(str(i-3).zfill(2), self.grid[i])
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
    
    def applyAll(self):
        for i in range(3, self.grid_height):
            for j in range(self.grid_width):
                self.applyFromPoint(j, i)
    
    def gravityAllPoints(self):
        for i in range(self.grid_height-2, 2, -1):
            for j in range(self.grid_width):
                y = i
                while y < self.grid_height-1 and self.grid[y+1][j] == self.hole:
                    self.grid[y][j], self.grid[y+1][j] = self.grid[y+1][j], self.grid[y][j]
                    y += 1

    
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
        while i != -1 and j != -1 and i != self.grid_width and j != self.grid_height and self.grid[j][i] == self.grid[y][x]:
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
    #directions = {"\x1b[A" : 'up', "\x1b[B" : 'down', "\x1b[D" : 'left', "\x1b[C" : 'right'}
    directions = {keyboard.Key.up : 'up', keyboard.Key.down : 'down', keyboard.Key.left : 'left', keyboard.Key.right : 'right'}
    newGame = grid()
    newGame.generateBottomGrid(1, True)
    newGame.generateBars()
    newGame.applyAll()
    def on_press(key):
        if key in directions:
            newGame.moveBar(directions[key])
        elif key == keyboard.KeyCode(vk=0, char='/', is_dead=False):
            newGame.rotateBar()
        elif key == keyboard.Key.enter:
            newGame.dropBar()
    def on_release(key):
        #print("on_release")
        pass
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    while True:
        # Refresh screen
        subprocess.call("clear")
        newGame.displayGrid()
        newGame.gravityDrop()
        '''
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
        '''
    listener.stop()
if __name__ == "__main__":
    main()