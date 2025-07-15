from User.User import UserManager
from MazeGeneration.MazeMatrix import MazeGenerator
from MazeGeneration.MazePlayer import MazePlayerDisplay

def main():
    user = UserManager()
    user.launch_login_ui()

    generator = MazeGenerator(user.difficulty)
    maze = generator.generate_maze()

    MazePlayerDisplay(maze, user)

if __name__ == "__main__":
    main()
