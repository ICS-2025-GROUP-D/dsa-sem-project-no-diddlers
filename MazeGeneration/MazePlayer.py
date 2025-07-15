import tkinter as tk
from tkinter import messagebox
from User.User import UserManager

class MazePlayerDisplay:
    def __init__(self, maze, user: UserManager, cell_size=20):
        self.maze = maze
        self.user = user
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.cell_size = cell_size
        self.goal_pos = self.find_goal_position()

        self.window = tk.Tk()
        self.window.title("Maze Player")

        self.canvas = tk.Canvas(
            self.window, width=self.cols * cell_size, height=self.rows * cell_size
        )
        self.canvas.pack()

        self.player_pos = [1, 1]
        self.draw_maze()
        self.draw_goal()
        self.draw_player()

        self.window.bind("<Up>", self.move_up)
        self.window.bind("<Down>", self.move_down)
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<Right>", self.move_right)

        self.window.mainloop()

    def find_goal_position(self):
        # Find the last open cell (bottom-right most '1')
        for r in range(self.rows - 1, 0, -1):
            for c in range(self.cols - 1, 0, -1):
                if self.maze[r][c] == 1:
                    return (r, c)
        return (self.rows - 2, self.cols - 2)

    def draw_cell(self, r, c, color):
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

    def draw_maze(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = "white" if self.maze[r][c] == 1 else "black"
                self.draw_cell(r, c, color)

    def draw_player(self):
        r, c = self.player_pos
        self.draw_cell(r, c, "green")

    def draw_goal(self):
        r, c = self.goal_pos
        self.draw_cell(r, c, "red")

    def move_player(self, dr, dc):
        new_r = self.player_pos[0] + dr
        new_c = self.player_pos[1] + dc

        if (
            0 <= new_r < self.rows and
            0 <= new_c < self.cols and
            self.maze[new_r][new_c] == 1
        ):
            self.draw_cell(*self.player_pos, "white")  # clear
            self.player_pos = [new_r, new_c]
            self.draw_player()

            if tuple(self.player_pos) == self.goal_pos:
                self.player_wins()

    def move_up(self,event): self.move_player(-1, 0)
    def move_down(self,event): self.move_player(1, 0)
    def move_left(self,event): self.move_player(0, -1)
    def move_right(self,event): self.move_player(0, 1)

    def player_wins(self):
        messagebox.showinfo("Victory!", f"You reached the goal, {self.user.username}!")
        self.user.update_score()

        self.window.destroy()
        self.user.launch_login_ui()  # Restart from login
