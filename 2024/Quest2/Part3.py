# Part 3 - Some edge case I cannot find, 11393 is not the right answer but I cannot construct a test case which gives the wrong answer.
# I am only missing 104 out of 11497 characters so it's not a common case. While it is wrong, it is damn fast (11x faster than the solution I saw on reddit which gives the right answer).

import time
import os, sys

def main():
    with open(os.path.join(sys.path[0],"Part3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    words = lines[0].split(":")[1].split(",")
    word_graph = {}

    for word in words:
        word_list = list(word)
        for idx in range(1, len(word_list)):
            try:
                word_graph[''.join(word_list[:idx])].add(word_list[idx])
            except:
                word_graph[''.join(word_list[:idx])] = set(word_list[idx])
        word_graph[''.join(word_list)] = set()

    grid = lines[2:]
    num_lines = len(grid)
    line_length = len(grid[0])
    letter_matrix = [[['',0] for _ in range(line_length)] for _ in range(num_lines)]

    # Generate the letter grid
    for i in range(num_lines):
        for j in range(line_length):
            letter_matrix[i][j] = [grid[i][j], 0]

    # Do 1 direction at a time, for each letter, check if that letter and the next are in our word graph and continue but with the two letters combined for the next check
    for di, dj in [[1,0], [0,1], [-1,0], [0,-1]]:
        for i in range(num_lines):
            for j in range(line_length):

                current_string = letter_matrix[i][j][0]
                current_i = i
                current_j = j
                go_next_letter = False

                while go_next_letter == False:

                    if current_string in word_graph.keys():
                        valid_next_letters = word_graph[current_string]

                        if current_string in words:
                            word_length = len(current_string)

                            # Mark all letters in this word as used
                            for k in range(word_length):
                                letter_matrix[(i + (di * k)) % num_lines][(j + (dj * k)) % line_length][1] = 1
                                            
                        # update which column we are in
                        current_j += dj
                        current_j = current_j % line_length

                        # update which row we are in
                        current_i += di

                        if current_i >= num_lines or current_i < 0:
                            # Reach the bottom/top of the grid
                            go_next_letter = True
                            continue

                        next_letter = letter_matrix[current_i][current_j][0]

                        if next_letter in valid_next_letters:
                            current_string += next_letter
                        else:
                            go_next_letter = True
                    
                    else:
                        go_next_letter = True

    count = 0
    for i in range(num_lines):
        for j in range(line_length):
            count += letter_matrix[i][j][1]

    print(count)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")