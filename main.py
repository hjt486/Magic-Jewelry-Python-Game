import time
import subprocess
class grid:
    def __init__(self):
        self.grid = [
        ['b', 'r', 'y', 'g', 'p', 'o'], 
        ['o', 'p', 'g', 'y', 'r', 'b'], 
        ['b', 'y', 'g', 'y', 'r', 'b'], 
        ['p', 'b', 'y', 'g', 'b', 'r'],
        ['p', 'b', 'g', 'b', 'r', 'g'],
        ['b', 'p', 'b', 'y', 'g', 'g']]
    
    def displayGrid(self):
        subprocess.call("clear")
        x_number_bar = []
        for i in range(len(self.grid[0])):
            x_number_bar.append(str(i))
        print(' ', x_number_bar)
        for i, row in enumerate(self.grid):
            print(i, row)
    
    def changePoint(self, x, y, color):
        self.grid[y][x] = color
        points_to_be_removed = set()
        directions = ['left', 'right', 'up', 'down', 'upleft', 'upright', 'downleft', 'downright']
        for direction in directions:
            points_to_be_removed |= self.findChain(x,y, direction)
        #print(points_to_be_removed)
        for i, j in points_to_be_removed:
            self.grid[j][i] = 'X'
    
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
    newGame = grid()
    newGame.displayGrid()

    while True:
        user_input = input("Please give x, y and a color like '0 1 r':")
        user_input = user_input.split(' ')
        user_input[0], user_input[1] = int(user_input[0]), int(user_input[1])
        newGame.changePoint(user_input[0], user_input[1], user_input[2])
        newGame.displayGrid()

if __name__ == "__main__":
    main()