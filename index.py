"""
The layout of the ship (walls, hallways, etc) is on a square grid, generated in the following way:
• Start with a square grid, D × D, of ‘blocked’ cells. Define the neighbors of cell as the adjacent cells in the
up/down/left/right direction. Diagonal cells are not considered neighbors.
• Choose a square in the interior to ‘open’ at random.
• Iteratively do the following:
– Identify all currently blocked cells that have exactly one open neighbor.
– Of these currently blocked cells with exactly one open neighbor, pick one at random.
– Open the selected cell.
– Repeat until you can no longer do so.
• Identify all cells that are ‘dead ends’ - open cells with one open neighbor.
• For approximately half these cells, pick one of their closed neighbors at random and open it.
Note: How big an environment D you can manage is going to depend on your hardware and implementation, but you
should aim to generate data on as large an environment as is feasible.

"""

#• Start with a square grid, D × D, of ‘blocked’ cells.

import random

def generateshiplayout(D = 3):
    grid = []

    for _ in range(D):
        row = []
        for _ in range(D):
            row.append("blocked")
        grid.append(row)
        
    #testing purposes of seeing the ship clearly
    
    for row in grid:
        print(" ".join(row))
        
    #Choose a square in the interior to ‘open’ at random.
    
    random_x_coordinate = random.randint(0, D-1)
    random_y_coordinate = random.randint(0, D-1)
    grid[random_x_coordinate][random_y_coordinate] = "open"
    
    for row in grid: 
        print(" ".join(row))

    
    """"
    Iteratively do the following:
    Identify all currently blocked cells that have exactly one open neighbor.
    Of these currently blocked cells with exactly one open neighbor, pick one at random.
    Open the selected cell.
    Repeat until you can no longer do so.
    
    """
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    
    def count_neighbors_helper(x,y):
        
        count = 0
        
        for addedx, addedy in directions: 
            fullx,fully = x + addedx, y + addedy
            if 0 <= fullx < D and 0 <= fully < D and grid[fullx][fully] == "open":
                count += 1
        return count
        
        
    
    while True: 
        
        one_neighbor_blocked_cells = []
        
        for x in range(0, D):
            for y in range(0, D):
                if grid[x][y] == "blocked" and count_neighbors_helper(x,y) == 1:
                    one_neighbor_blocked_cells.append((x,y))
                    
        if not one_neighbor_blocked_cells:
            break
        
        x,y = random.choice(one_neighbor_blocked_cells)
        
        grid[x][y] = "open"
        
    
    for row in grid: 
        print(" ".join(row))
    
    
    #Identify all cells that are ‘dead ends’ - open cells with one open neighbor.
        
    dead_ends = []
    
    for x in range(0, D):
        for y in range(0, D):
            if grid[x][y] == "open" and count_neighbors_helper(x, y) == 1:
                dead_ends.append((x, y))
    print("Dead Ends")
    
    
    for x, y in dead_ends:
        print(f"({x}, {y})")
                
            
                    
generateshiplayout()
            
        
