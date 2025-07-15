import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from Users import LeaderboardLinkedList

class UserManager:
    def __init__(self):
        self.username = None
        self.difficulty = "Easy"
        self.score = 0
        self.connection = self._create_connection()
        self.leaderboard = LeaderboardLinkedList()

    def _create_connection(self):
        """Establish connection to MySQL database"""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mazerunner"
            )
            return connection
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None

    def get_or_create_user(self, username: str) -> bool:
        """Check if user exists or create new user"""
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor(dictionary=True)

            # Check if user exists
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                self.username = user['username']
                self.score = user['score']
                return False  # Existing user
            else:
                # Create new user
                cursor.execute(
                    "INSERT INTO Users (username) VALUES (%s)",
                    (username,)
                )
                self.connection.commit()
                self.username = username
                self.score = 0
                return True  # New user
        except Error as e:
            messagebox.showerror("Database Error", f"Error accessing user data: {e}")
            return False

    def update_score(self):
        """Update user's score based on current difficulty"""
        if not self.username or not self.connection:
            return

        difficulty_points = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3
        }
        points = difficulty_points.get(self.difficulty, 1)

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE Users SET score = score + %s WHERE username = %s",
                (points, self.username)
            )
            self.connection.commit()

            # Update in-memory leaderboard
            self.leaderboard.insert_sorted(self.username, self.score + points)
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update score: {e}")

    def delete_user(self, username: str) -> bool:
        """Delete user from database"""
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM Users WHERE username = %s",
                (username,)
            )
            self.connection.commit()

            # Update leaderboard
            if cursor.rowcount > 0:
                self.leaderboard.remove_user(username)
                return True
            return False
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete user: {e}")
            return False

    def show_leaderboard(self):
        """Display leaderboard from database"""
        if not self.connection:
            return

        try:
            # Load fresh data from database
            self.leaderboard = LeaderboardLinkedList()
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT username, score FROM Users ORDER BY score DESC LIMIT 10"
            )

            for username, score in cursor:
                self.leaderboard.insert_sorted(username, score)

            # Display UI (existing code)
            leaderboard_window = tk.Toplevel()
            leaderboard_window.title("Leaderboard")
            leaderboard_window.geometry("300x400")

            tk.Label(leaderboard_window,
                    text="🏆 Leaderboard",
                    font=("Arial", 16, "bold")).pack(pady=10)

            frame = tk.Frame(leaderboard_window)
            frame.pack(pady=5)

            leaderboard = self.leaderboard.to_list()
            for idx, (username, score) in enumerate(leaderboard, start=1):
                tk.Label(frame,
                        text=f"{idx}. {username} - {score} pts", 
                        font=("Arial", 12)).pack(anchor="w", padx=10)

            tk.Button(leaderboard_window,
                    text="Close",
                    command=leaderboard_window.destroy).pack(pady=10)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load leaderboard: {e}")

    def launch_login_ui(self):
        """Launch the login UI (existing code with database integration)"""
        def on_submit():
            username = username_entry.get().strip()
            difficulty = difficulty_var.get()

            if not username:
                messagebox.showerror("Input Error", "Username cannot be empty.")
                return

            if self.get_or_create_user(username):
                messagebox.showinfo("Welcome", f"New user created!\nUsername: {username}\nDifficulty: {difficulty}")
            else:
                messagebox.showinfo("Welcome Back", f"Welcome back {username}!\nCurrent Score: {self.score}\nDifficulty: {difficulty}")

            self.difficulty = difficulty
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

        tk.Button(login_window,
                text="View Leaderboard",
                command=self.show_leaderboard,
                font=("Arial", 10)).pack(pady=5)

        tk.Button(login_window,
                text="Start Game",
                command=on_submit,
                font=("Arial", 12)).pack(pady=15)

        tk.Button(login_window,
                text="Delete Account",
                command=lambda: self._confirm_delete(username_entry.get()),
                font=("Arial", 10),
                fg="red").pack(pady=5)

        login_window.mainloop()

    def _confirm_delete(self, username):
        """Confirm and handle user deletion"""
        if not username:
            return

        if messagebox.askyesno("Confirm", f"Delete {username} and all data?"):
            if self.delete_user(username):
                messagebox.showinfo("Success", "User deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete user or user not found.")

    def __del__(self):
        """Clean up database connection"""
        if self.connection:
            self.connection.close()