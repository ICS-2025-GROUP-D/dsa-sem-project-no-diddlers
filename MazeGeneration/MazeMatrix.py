import random

class MazeGenerator:
    def __init__(self, difficulty):
        self.rows, self.cols = self.get_maze_size(difficulty)
        self.maze = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.stack = []

    def get_maze_size(self, difficulty):
        sizes = {
            "Easy": (11, 11),
            "Medium": (21, 21),
            "Hard": (31, 31)
        }
        return sizes.get(difficulty, (11, 11))

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)
        result = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and not self.visited[nr][nc]:
                result.append((nr, nc))
        return result 
    
    def generate_maze(self):
   
        start_r, start_c = 1, 1
        self.maze[start_r][start_c] = 1
        self.visited[start_r][start_c] = True
        self.stack.append((start_r, start_c))

        while self.stack:
            r, c = self.stack[-1]
            neighbors = self.neighbors(r, c)

        if neighbors:
            nr, nc = random.choice(neighbors)
            wall_r, wall_c = (r + nr) // 2, (c + nc) // 2
            self.maze[wall_r][wall_c] = 1
            self.maze[nr][nc] = 1
            self.visited[nr][nc] = True
            self.stack.append((nr, nc))
        else:
            self.stack.pop()

        return self.maze

 
