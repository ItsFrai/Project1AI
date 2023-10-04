import random
import time
import heapq

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
        
        # initial positions of bot, button, fire
        self.bot = (-1, -1)
        self.button = (-1, -1)
        self.fire = (-1, -1)

    def __repr__(self) -> str:
        ship_str = ""
        for row in self.ship:
            ship_str += '[' + ' '.join(row) + ']\n'
        return ship_str
    
    def heuristic(self, x, y, curr_x, curr_y):
        return abs(x - curr_x) + abs(y - curr_y)

    
    # generates and returns a colored block
    def colored_block(self, color: str) -> str:
        color_codes = {
            'r': '\033[31m',  # Red
            'g': '\033[32m',  # Green
            'b': '\033[34m',  # Blue
            'y': '\033[33m',  # Yellow
            'm': '\033[35m',  # Magenta
            'c': '\033[36m',  # Cyan
            'w': '\033[37m',  # White
        }

        reset_color = '\033[0m'

        if color in color_codes:
            return f"{color_codes[color]}\u2588{reset_color}"
        else:
            return f"Invalid color code: {color}"
    
    # given a cordinate and what you're looking for, it will return number of neighbors next to an open cells
    def count_neighbors(self, x: int, y: int, item: str) -> int:
        count = 0
        for move_x, move_y in self.directions: 
            new_x, new_y = x + move_x, y + move_y
            if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == item:
                count += 1
        return count
    
    def generate_ship(self) -> None:
        for _ in range(self.D):
            row = ['X'] * self.D
            self.ship.append(row)
        
        # set of all possible square to open
        open_possibilities = set()
        
        #Choose a square in the interior to ‘open’ at random.
        rand_x_coord = random.randint(0, self.D-1)
        rand_y_coord = random.randint(0, self.D-1)
        self.ship[rand_x_coord][rand_y_coord] = 'O'


        open_possibilities.add((rand_x_coord, rand_y_coord))


        print(f"\nOpening inital.... {rand_x_coord, rand_y_coord}")
        print(self)

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
        print(self)

        # now get intial num of deadends
        for x in range(self.D):
            for y in range(self.D):
                if self.ship[x][y] == 'O' and self.count_neighbors(x, y, "O") == 1:
                    self.dead_ends.append((x, y))

        half = len(self.dead_ends) // 2
        print(f"Number of deadends (init): {len(self.dead_ends)}")

        # make approximately half of deadends non dead ends
        while len(self.dead_ends) > half:
            curr_x, curr_y = random.choice(self.dead_ends)
            print(f"Removing: {curr_x, curr_y} from dead ends")
            self.dead_ends.remove((curr_x,curr_y))

            # Remove one of the sides arbitrarily from the dead ends
            for x, y in random.sample(self.directions, len(self.directions)):
                new_x, new_y = x + curr_x, y + curr_y
                if  0 <= new_x < self.D and 0 <= new_y < self.D and (self.ship[new_x][new_y] in ['X', '-']):
                    self.ship[new_x][new_y] = 'O'
                    break

            print(self)
            new_dead_ends = [] # new deadend array to see how many deadends are removed
 
            # recompute the num of deadends
            for x in range(self.D):
                for y in range(self.D):
                    if self.ship[x][y] == 'O' and self.count_neighbors(x, y, "O") == 1:
                        new_dead_ends.append((x,y))
 
            self.dead_ends = new_dead_ends.copy()

            for x in range(self.D):
                for y in range(self.D):
                    if self.ship[x][y] == '-':
                        self.ship[x][y] = 'X' 

        print(f"Length of deadends: {len(self.dead_ends)}\n" ,"Dead ends:")
        for x, y in self.dead_ends:
            print(f"({x}, {y})")
        print()
        
        # randomly chooses locations for a button, bot, and fire
        while self.bot == (-1, -1) or self.button == (-1, -1) or self.fire == (-1, -1):
            rand_x_coord = random.randint(0, self.D-1)
            rand_y_coord = random.randint(0, self.D-1)
            
            if self.ship[rand_x_coord][rand_y_coord] == 'O':
                if self.bot == (-1, -1):
                    self.ship[rand_x_coord][rand_y_coord] = self.colored_block('c')
                    self.bot = (rand_x_coord, rand_y_coord)
                elif self.button == (-1, -1):
                    self.ship[rand_x_coord][rand_y_coord] = self.colored_block('g')
                    self.button = (rand_x_coord, rand_y_coord)
                elif self.fire == (-1, -1):
                    self.ship[rand_x_coord][rand_y_coord] = self.colored_block('r')
                    self.fire = (rand_x_coord, rand_y_coord)

    def run_bot_1(self) -> None: # run with the type of bot you want
        possible_places = [self.colored_block('c'), 'O']
        fire_possibilties = set()
        q = .9 # ???
        curr_x, curr_y = self.fire

        # Initial fire probable locations (up to 4)
        for x, y in self.directions:
            new_x, new_y = x + curr_x, y + curr_y
            if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == 'O':
                fire_possibilties.add((new_x, new_y)) 
                print((new_x, new_y))

        while self.bot not in fire_possibilties or self.bot == self.button:
            fire_copy = fire_possibilties.copy()

            for fire_poss in fire_possibilties:
                curr_x, curr_y = fire_poss
                k = self.count_neighbors(new_x, new_y, self.colored_block('r')) # number of fires
                fire_spread_possibility = 1 - (1 - q) ** k
                rand = random.random()
                print(f"Fire spread: {fire_spread_possibility}")
                print(f"rand: {rand}")
                if fire_spread_possibility > rand:
                    self.ship[curr_x][curr_y] = self.colored_block('r')
                    for x, y in self.directions:
                        new_x, new_y = x + curr_x, y + curr_y
                        if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] in possible_places:
                            fire_copy.add((new_x, new_y))
                else:
                    fire_copy.add(self.fire)
            fire_possibilties = fire_copy.copy()
            print(self)
            time.sleep(3)
            
             # fire_possibilties.remove(self.fire)
                # Forumla = 1 - (1 - q)^k  where k = number of burning cells next to this one
                # get the number of neighbors that are on fire --> k
                # if neighbors are all on fire, remove it
                # else compute the formula and see if the random number is larger than it
                
    def run_bot_3(self) -> None:
        
        possible_places = [self.colored_block('c'), 'O']

        fire_possibilities = set()
        
        curr_x, curr_y = self.fire
        
        actual_fire = set()
        
        actual_fire.add((curr_x,curr_y))
        
        q = 0.9

        for x, y in self.directions:
            new_x, new_y = x + curr_x, y + curr_y
            if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == 'O':
                fire_possibilities.add((new_x, new_y))

        while self.bot not in actual_fire or self.bot != self.button:
            
            def find_shortest_path(bot_x, bot_y, button_x, button_y, actual_fire):
                
                 #finds the adjacent cells of the fire and combine with actual fire for bot to ignore 

                adjacent_cells_from_fire = set()

                for x, y in actual_fire:
                    for dx, dy in self.directions:
                        adj_x, adj_y = x + dx, y + dy
                        if 0 <= adj_x < self.D and 0 <= adj_y < self.D and self.ship[adj_x][adj_y] == "O":
                            adjacent_cells_from_fire.add((adj_x, adj_y))

                combination_of_avoided_cells = actual_fire.union(adjacent_cells_from_fire)
                
                

                queue = [(0, (bot_x, bot_y))]
                heapq.heapify(queue)

                cost = {}
                parent = {}

                cost[(bot_x, bot_y)] = 0

                while queue:
                    _, current = heapq.heappop(queue)

                    c_x, c_y = current

                    if c_x == button_x and c_y == button_y:
                        path = []

                        while current in parent:
                            path.insert(0, current)
                            current = parent[current]
                        return path

                    for dx, dy in self.directions:
                        new_x, new_y = c_x + dx, c_y + dy
                        new_pos = (new_x, new_y)

                        if (0 <= new_x < self.D and 0 <= new_y < self.D 
                            and self.ship[new_x][new_y] not in combination_of_avoided_cells 
                            and self.ship[new_x][new_y] != 'X'):
                            new_cost = cost[current] + 1

                            if (new_pos not in cost or new_cost < cost[new_pos]):
                                cost[new_pos] = new_cost
                                priority = new_cost + self.heuristic(button_x, button_y, new_x, new_y)
                                heapq.heappush(queue, (priority, new_pos))
                                parent[new_pos] = current

                return None

            button_path = find_shortest_path(self.bot[0], self.bot[1], self.button[0], self.button[1], actual_fire)

            if button_path:
                self.ship[self.bot[0]][self.bot[1]] = 'O'
                self.bot = button_path[0]
                self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                
            if self.bot == self.button:
                print("Bot won")
                break
            if self.bot in fire_possibilities:
                print("you lost")
                break
        
            fire_copy = fire_possibilities.copy()
        
            for fire_pos in fire_possibilities:
                curr_x, curr_y = fire_pos
                k = self.count_neighbors(curr_x, curr_y, self.colored_block('r'))
                fire_spread_probability = 1 - (1 - q) ** k
                rand = random.random()

                if fire_spread_probability > rand:
                    self.ship[curr_x][curr_y] = self.colored_block('r')
                    actual_fire.add((curr_x,curr_y))
                    for x, y in self.directions:
                        new_x, new_y = x + curr_x, y + curr_y
                        if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] in possible_places:
                            fire_copy.add((new_x, new_y))
                else:
                    fire_copy.add(self.fire)

            fire_possibilities = fire_copy.copy()
            print(self)
            time.sleep(3)
    
#oooggsdgfasgh
               
if __name__ == "__main__":

    ship = Ship()
    ship.generate_ship()
    print(ship)
    # ship.generate_init_ship()
    ans = int(input("Which bot do you want to run?\n1.Bot 1\n2.Bot 2.\n3.Bot 3\n4.Bot 4\n"))
    
    
    if ans == 1:
        ship.run_bot_1()
    elif ans == 2:
        ship.run_bot_2()
    elif ans == 3:
        ship.run_bot_3()
    

