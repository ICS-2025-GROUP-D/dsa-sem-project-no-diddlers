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
 
