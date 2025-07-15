import tkinter as tk
import time

class MazeGraphDisplay:
    def __init__(self, maze, cell_size=20):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.cell_size = cell_size
        self.graph = self.build_graph()

        self.window = tk.Tk()
        self.window.title("Maze Graph Viewer")
        self.canvas = tk.Canvas(
            self.window, width=self.cols * cell_size, height=self.rows * cell_size
        )
        self.canvas.pack()

    def build_graph(self):
        graph = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == 1:
                    node = (r, c)
                    graph[node] = []
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < self.rows
                            and 0 <= nc < self.cols
                            and self.maze[nr][nc] == 1
                        ):
                            graph[node].append((nr, nc))
        return graph

    def draw_cell(self, r, c, color):
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

    def render_maze_with_stack_traversal(self):
        visited = set()
        stack = [(1, 1)]

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue

            visited.add((r, c))
            self.draw_cell(r, c, "white")
            self.window.update()
            time.sleep(0.001)

            for neighbor in self.graph.get((r, c), []):
                stack.append(neighbor)

        self.window.mainloop()
