import sys, os, time

def main():
    with open(os.path.join(sys.path[0], "Part2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.splitlines()
    grid = lines
    width = len(grid[0])
    height = len(grid)

    for j in range(height):
        grid[j] = list(grid[j])

    changes_made = True
    counter = 0
    while changes_made == True:
        counter += 1
        print(f"Iteration {counter}")
        changes_made = False

        for i in range(width):
            for j in range(height):

                tile = grid[j][i]

                if tile == '.':
                    grid[j][i] = 0
                    changes_made = True

                if tile == '#':
                    grid[j][i] = 1
                    changes_made = True
                adj_tiles = [None, None, None, None]
                try:
                    adj_tiles[3] = grid[j][i-1]
                except:
                    adj_tiles.pop()
                
                try:
                    adj_tiles[2] = grid[j][i+1]
                except:
                    adj_tiles.pop(2)

                try:
                    adj_tiles[1] = grid[j-1][i]
                except:
                    adj_tiles.pop(1)

                try:
                    adj_tiles[0] = grid[j+1][i]
                except:
                    adj_tiles.pop(0)
                
                if type(tile) == int and tile != 0:
                    should_increase = True
                    for adj_tile in adj_tiles:
                        if adj_tile < tile:
                            should_increase = False
                        
                    if should_increase:
                        grid[j][i] += 1
                        changes_made = True
            
    for j in range(height):
        should_print = False
        for i in range(width):
            if grid[j][i] != 0:
                should_print = True
        if should_print:
            print(grid[j])

    total = 0
    for i in range(width):
        for j in range(height):
            total += grid[j][i]

    print(total)
                        

            

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")