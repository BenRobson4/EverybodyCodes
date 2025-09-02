import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"Part3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    runes = lines[0].split(":")[1].split(",")
    grid = lines[2:]
    width = len(grid[0])
    height = len(grid)
    found_indices = set()
    for rune in runes:
        rune_len = len(rune)
        # iterate over each row
        for row, line in enumerate(grid):
            line_len = len(line)
            if rune_len > line_len:
                continue
            for i in range(0, line_len):
                section = ""
                if i + rune_len < line_len:
                    section = line[i:i+rune_len]
                else:
                    section = line[i:] + line[:i+rune_len-line_len]
                if section == rune or section == rune[::-1]:
                    # print(f"Found {rune} at {row},{i}")
                    for j in range(i, i+rune_len):
                        if j >= line_len:
                            found_indices.add((row, j-line_len))
                        else:
                            found_indices.add((row, j))
        # iterate over each column
        for col in range(width):
            if rune_len > height:
                continue
            for i in range(0, height - rune_len + 1):
                section = ""
                for w in range(0, rune_len):
                    section += grid[i+w][col]
                if section == rune or section == rune[::-1]:
                    # print(f"Found {rune} at {i},{col}")
                    for j in range(i, i+rune_len):
                        if j >= height:
                            found_indices.add((j-height, col))
                        else:
                            found_indices.add((j, col))
    print(len(found_indices))
                
        
            

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")