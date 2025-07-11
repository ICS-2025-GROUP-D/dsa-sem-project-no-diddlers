import tkinter as tk
from tkinter import messagebox
import json
import os
from .Users import LeaderboardLinkedList

USER_DB_FILE = "users.json"

class UserManager:
    def __init__(self):
        self.username = None
        self.difficulty = "Easy"
        self.score = 0

    def load_users(self):
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_users(self, users):
        with open(USER_DB_FILE, "w") as file:
            json.dump(users, file, indent=4)

    def get_or_create_user(self, username):
        users = self.load_users()

        for user in users:
            if user["username"] == username:
                self.score = user["score"]
                return False  # Existing user

        new_user = {
            "username": username,
            "score": 0
        }
        users.append(new_user)
        self.save_users(users)
        self.score = 0
        return True  # New user

    def update_score(self):
        if not self.username:
            return

        users = self.load_users()

        # Points based on difficulty
        difficulty_points = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3
        }
        points = difficulty_points.get(self.difficulty, 1)

        for user in users:
            if user["username"] == self.username:
                user["score"] += points
                self.score = user["score"]  # update in memory too
                break

        self.save_users(users)

    def show_leaderboard(self):
        users = self.load_users()

        linked_list = LeaderboardLinkedList()
        for user in users:
            linked_list.insert_sorted(user["username"], user["score"])

        leaderboard_window = tk.Toplevel()
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("300x400")
        leaderboard_window.resizable(False, False)

        tk.Label(leaderboard_window, text="🏆 Leaderboard", font=("Arial", 16, "bold")).pack(pady=10)

        frame = tk.Frame(leaderboard_window)
        frame.pack(pady=5)

        leaderboard = linked_list.to_list()
        for idx, (username, score) in enumerate(leaderboard, start=1):
            tk.Label(frame, text=f"{idx}. {username} - {score} pts", font=("Arial", 12)).pack(anchor="w", padx=10)

        tk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy).pack(pady=10)

    def launch_login_ui(self):
        def on_submit():
            username = username_entry.get().strip()
            difficulty = difficulty_var.get()

            if not username:
                messagebox.showerror("Input Error", "Username cannot be empty.")
                return

            self.username = username
            self.difficulty = difficulty

            is_new = self.get_or_create_user(username)

            if is_new:
                messagebox.showinfo("Welcome", f"New user created!\nUsername: {username}\nDifficulty: {difficulty}")
            else:
                messagebox.showinfo("Welcome Back", f"Welcome back {username}!\nCurrent Score: {self.score}\nDifficulty: {difficulty}")

            login_window.destroy()

        login_window = tk.Tk()
        login_window.title("Maze Game - User Login")
        login_window.geometry("400x350")
        login_window.resizable(False, False)

        tk.Label(login_window, text="Enter your username:", font=("Arial", 12)).pack(pady=10)
        username_entry = tk.Entry(login_window, width=25, font=("Arial", 12))
        username_entry.pack(pady=5)

        tk.Label(login_window, text="Select Difficulty:", font=("Arial", 12)).pack(pady=10)
        difficulty_var = tk.StringVar(value="Easy")
        tk.OptionMenu(login_window, difficulty_var, "Easy", "Medium", "Hard").pack(pady=5)
        tk.Button(login_window, text="View Leaderboard", command=self.show_leaderboard, font=("Arial", 10)).pack(pady=5)

        tk.Button(login_window, text="Start Game", command=on_submit, font=("Arial", 12)).pack(pady=15)
        tk.Button(login_window, text="Exit", command=login_window.quit, font=("Arial", 10), fg="red").pack(pady=5)

        login_window.mainloop()
