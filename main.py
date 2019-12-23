import subprocess
import time
import random

class grid:
    def __init__(self):
        # Create 6 x 13 grid
        self.hole = '-'
        self.grid = [[self.hole] * 6 for i in range(14)]
        #self.color = ['b', 'r', 'y', 'g', 'p', 'o']
        self.color = ['✤', '✹', '✿', '♣', '♦', '♥']
        self.bar = []
        self.bar_position = []
    
    def generateBottomGrid(self, height, ladder = False):
        for j in range(len(self.grid) - height, len(self.grid)):
            for i in range(len(self.grid[0])):
                self.grid[j][i] = self.color[random.randrange(0, 6)]
        if ladder == True:
            x = 0
            for j in range(len(self.grid)-2, len(self.grid)-1-height-1, -1):
                x += 1
                for i in range(len(self.grid[0])-1, len(self.grid[0])-1-x, -1):
                    self.grid[j][i] = self.hole
    
    def generateBar(self):
        self.bar.clear()
        self.bar_position.clear()
        for i in range(3):
            # Generate random number from self.color for a bar at original position
            point = self.color[random.randrange(0, 6)]
            self.bar.append(point)
            self.grid[i][3] = point
            self.bar_position = [(3, 0),(3, 1),(3, 2)]
    
    def moveBar(self, direction) -> bool:
        direction_list = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        # a and b is the next direction step
        a, b = direction_list[direction][0], direction_list[direction][1]
        element1x, element1y = self.bar_position[0][0], self.bar_position[0][1]
        element2x, element2y = self.bar_position[1][0], self.bar_position[1][1]
        element3x, element3y = self.bar_position[2][0], self.bar_position[2][1]
        width = len(self.grid[0])
        height = len(self.grid)
        # Left right, up down edges
        if element1x + a < 0 or element1x + a > width - 1 or element1y + b < 0 or element3y + b > height - 1:
            return False
        # Detect surrounding if occupied
        if direction == 'left' or direction == 'right':
            if self.grid[element1y][element1x+a] != self.hole or self.grid[element2y][element2x+a] != self.hole or self.grid[element3y][element3x+a] != self.hole:
                return False
        if direction == 'up' and self.grid[element1y - 1][element1x] != self.hole or direction == 'down' and self.grid[element3y + 1][element1x] != self.hole:
            return False
        # This is to prevent wrong lagging values
        if direction == 'up' or direction =='left' or direction == 'right':
            start = 0
            end = 3
            step = 1
        elif direction == 'down':
            start = 2
            end = -1
            step = -1
        # Move by exchanging
        for k in range(start, end, step):
            i, j = self.bar_position[k]
            print(a, b)
            self.grid[j][i], self.grid[j+b][i+a] = self.grid[j+b][i+a], self.grid[j][i]
            self.bar_position[k] = (i+a, j+b)
        return True
    
    def rotateBar(self):
        self.bar[0], self.bar[1], self.bar[2] = self.bar[2], self.bar[0], self.bar[1]
        for k, (x, y) in enumerate(self.bar_position):
            self.grid[y][x] = self.bar[k]

    def dropBar(self):
        for i in range(3):
            self.applyFromPoint(self.bar_position[i][0], self.bar_position[i][1])
        self.generateBar()

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
    
    def applyFromPoint(self, x, y):
        points_to_be_removed = set()
        directions = ['left', 'right', 'up', 'down', 'upleft', 'upright', 'downleft', 'downright']
        for direction in directions:
            points_to_be_removed |= self.findChain(x,y, direction)
        #print(points_to_be_removed)
        for i, j in points_to_be_removed:
            self.grid[j][i] = self.hole
    
    def findChain(self, x, y, direction):
        direction_pointer = {
            'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1),
            'upleft': (-1, -1), 'upright': (1, -1), 'downleft': (-1, 1), 'downright': (1, 1)}
        a, b = direction_pointer[direction]
        chain = {(x,y)}
        i, j = x, y
        counter = 0
        #print(self.grid)
        while i != -1 and j != -1 and i != len(self.grid[0]) and j != len(self.grid) and self.grid[j][i] == self.grid[y][x]:
            chain.add((i, j))
            counter += 1
            i += a
            j += b
            #print('current at',direction, i, j)
        #print('counter', counter)
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