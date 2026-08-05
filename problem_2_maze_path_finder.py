"""
Maze Path Finder using Backtracking Algorithm

Algorithm:
    Backtracking (Recursive Search)

Description:
    This program finds a valid path through a maze
    from a starting point (S) to an ending point (E).

Symbols:
    S = Starting point
    E = Ending point
    0 = Open path
    1 = Wall
    * = Correct path
"""


# ==============================================
# Function: print_maze()
#
# Purpose:
#   Presents the maze clearly, allowing users 
#   to compare the original maze and the 
#   solved maze after applying the algorithm.
# ==============================================
def print_maze(maze):
    for row in maze:
        print(" ".join(row))
    print()



# =====================================
# Function: find_start_end()
#
# Purpose:
#   Finds the coordinates of S and E
#   which acts as the start and end
#   off the maze.
# =====================================
def find_start_end(maze):
    start = None
    end = None
    for a in range(len(maze)):
        for b in range(len(maze[a])):
            if maze[a][b] == "S":
                start = (a, b)
            elif maze[a][b] == "E":
                end = (a, b)
    return start, end



# =================================================
# Function: is_valid_move()
#
# Purpose:
#   Checks whether a movement is allowed.
#
# NOTE:
#   The "constraint checking" part of backtracking.
#
#   A position is valid when:
#       1. It is inside the maze's boundary
#       2. It is not a wall
#       3. It has not already been visited
#
#   Invalid choices are immediately rejected
#   to eliminate unecessary searching.
# ==================================================
def is_valid_move(maze, visited, x, y):
    rows = len(maze)
    cols = len(maze[0])
    return (
        x >= 0 and
        x < rows and
        y >= 0 and
        y < cols and
        maze[x][y] != "1" and
        not visited[x][y]
    )



# ====================================================
# Function: solve_maze()
#
# Purpose:
#   Main backtracking algorithm.
#
#NOTE:
#   The algorithm explores possible paths recursively.
#
#   If the chosen path reaches a dead end:
#       1. Remove the current decision
#       2. Return to the previous position
#       3. Try another possible direction
# ====================================================
def solve_maze(maze, visited, x, y, path):
    # Destination reached
    if maze[x][y] == "E":
        path.append((x, y))
        return True
    
    # Marks the current coordinate as visited
    visited[x][y] = True

    # Stores the current position
    path.append((x, y))

    # Possible movements in order:
    # Down, Up, Right, Left
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    for dx, dy in directions:
        new_x = x + dx
        new_y = y + dy
        if is_valid_move(
            maze,
            visited,
            new_x,
            new_y
        ):
            if solve_maze(
                maze,
                visited,
                new_x,
                new_y,
                path
            ):
                return True

    # =================================================
    # Backtracking step
    #
    # If the current path does not lead to the
    # destination, remove the current decision 
    # and try another possible route.
    # =================================================

    path.pop()
    return False



# ====================================================
# Function: mark_solution()
#
# Purpose:
#   Marks the final path using '*'.
#
# NOTE:
#   The path is separated from the searching process.
#   The algorithm stores coordinates first, then
#   displays the solution afterwards.
# ====================================================
def mark_solution(maze, path):
    solved_maze = [
        row[:] for row in maze
    ]

    for x, y in path:
        if solved_maze[x][y] != "S" and solved_maze[x][y] != "E":
            solved_maze[x][y] = "*"
    return solved_maze



# ========================================
# Function: validate_maze()
#
# Purpose:
#   Prevents input errors and ensures the 
#   algorithm receives a valid maze.
# ========================================
def validate_maze(maze):
    start_count = 0
    end_count = 0
    allowed_symbols = [
        "S",
        "E",
        "0",
        "1"
    ]

    for row in maze:
        for cell in row:
            if cell not in allowed_symbols:
                return False
            if cell == "S":
                start_count += 1
            if cell == "E":
                end_count += 1
    return start_count == 1 and end_count == 1



# ==============================================
# Function: get_maze_input()
#
# Purpose:
#     Collects the maze's layout from the user.
# ==============================================
def get_maze_input():
    while True:
        rows = int(input("Enter number of rows: "))
        cols = int(input("Enter number of columns: "))
        maze = []

        print("\nEnter maze rows:")
        print("S = Start | E = End | 0 = Path | 1 = Wall\n")

        for a in range(rows):
            while True:
                row = input(
                    f"Row {a+1}: "
                ).upper()
                if len(row) != cols:
                    print(
                        "Invalid row length. Try again."
                    )
                elif any(char not in ["S", "E", "0", "1"] for char in row):
                    print(
                        "Invalid character(s). Only S, E, 0 and 1 are allowed."
                        )
                else:
                    maze.append(
                        list(row)
                    )
                    break

        if validate_maze(maze):
            return maze
        else:
            print(
                "\nInvalid maze."
            )
            print(
                "Maze must contain exactly one S and one E."
            )
            maze.clear()



# =============
# MAIN PROGRAM
# =============
print("Maze Path Finder: Backtracking Algorithm")

maze = get_maze_input()

print("\nMaze layout:")
print("----------------")
print_maze(maze)

start, end = find_start_end(maze)
rows = len(maze)
cols = len(maze[0])

visited = [
    [False] * cols
    for _ in range(rows)
]
path = []

solution_exists = solve_maze(
    maze,
    visited,
    start[0],
    start[1],
    path
)

if solution_exists:
    solved_maze = mark_solution(
        maze,
        path
    )
    print("Path found")
    print("Solved Maze:")
    print("----------------")
    print_maze(solved_maze)

    print("Path coordinates:")
    print("----------------")
    for position in path:
        print(position)

    print(
        "\nTotal Steps:",
        len(path) - 1
    )

    visited_cells = sum(
        row.count(True)
        for row in visited
    )
    print(
        "Visited Cells:",
        visited_cells
    )

else:
    print(
        "No valid path exists."
    )

"""
5x5 maze test samples:

    Valid maze:
    S0011
    11000
    00010
    01110
    1E000

    Invalid maze:
    S0011
    11000
    00010
    01110
    1E100
"""