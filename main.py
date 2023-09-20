import random

class Ship():
    def __init__(self) -> None:
        try:
            D = int(input("Enter D x D Dimension: "))
        except ValueError as e:
            print("Needs to be an int")
            exit()
        except Exception as e:
            print(e)
            exit()
        
        # Up, down, left, right
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        self.D = D # D x D Dimension of ship
        self.ship = []
        self.dead_ends = []

    def __repr__(self) -> str:
        ship_str = ""
        for row in self.ship:
            ship_str += '[' + ' '.join(row) + ']\n'
        return ship_str

    def generate_init_ship(self):
        for _ in range(self.D):
            row = ['X'] * self.D
            self.ship.append(row)

        # Print the ship grid
        for row in self.ship:
            print('[', end='')
            print(' '.join(row), end='')
            print(']')
    
    # given a cordinate, it will return number of neighbors next to an open cells
    def count_neighbors(self, x: int, y: int) -> int:
        count = 0
        for move_x, move_y in self.directions: 
            new_x, new_y = x + move_x, y + move_y
            if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == "O":
                count += 1
        return count
    
    def open_ship(self) -> None:
        # set of all possible square to open
        open_possibilities = set()
        
        #Choose a square in the interior to ‘open’ at random.
        rand_x_coord = random.randint(0, self.D-1)
        rand_y_coord = random.randint(0, self.D-1)
        self.ship[rand_x_coord][rand_y_coord] = 'O'
        
        open_possibilities.add((rand_x_coord, rand_y_coord))
        
        print(f"\nOpening inital.... {rand_x_coord, rand_y_coord}")
        for row in self.ship:
            print(" ".join(row))
        print()

        while open_possibilities:
            curr_x, curr_y = open_possibilities.pop()
            self.ship[curr_x][curr_y] = 'O'

            for x, y in self.directions:
                new_x, new_y = x + curr_x, y + curr_y
                #if within the ship dimensions and is blocked
                if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == 'X':
                    # Check if the square is not already in open_possibilities
                    if (new_x, new_y) in open_possibilities:
                        open_possibilities.remove((new_x, new_y))
                        self.ship[new_x][new_y] = '-' # Not able to open
                    else:
                        open_possibilities.add((new_x,new_y))

        # now get deadends
        for x in range(self.D):
            for y in range(self.D):
                if self.ship[x][y] == "O" and self.count_neighbors(x, y) == 1:
                    self.dead_ends.append((x, y))
        
        print("Dead ends:")
        for x, y in self.dead_ends:
            print(f"({x}, {y})") 
        print()

if __name__ == "__main__":
    ship = Ship()
    ship.generate_init_ship()
    ship.open_ship()
    print(ship)
    # ship.generate_init_ship()
            
        
