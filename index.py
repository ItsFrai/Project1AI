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
2 The Bot
The bot occupies an open cell somewhere in the ship (to be determined shortly). The bot can move to one adjacent
cell every time step (up/down/left/right).
3 The Fire
At a random open cell, a fire starts. Every time step, the fire has the ability to spread to adjacent open cells. The fire
cannot spread to blocked cells. The fire spreads according to the following rules: At each timestep, a non-burning
cell catches on fire with the probability 1 − (1 − q)K :
• q is a parameter between 0 and 1, defining the flammability of the ship.
• K is the number of currently burning neighbors of this cell.

"""

#• Start with a square grid, D × D, of ‘blocked’ cells.



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
    
generateshiplayout()
            
        
