import time
import random
import matplotlib.pyplot as plt
from MazeMatrix import MazeGenerator
from MazeDisplay import MazeGraphDisplay

def test_dfs_generation(rows, cols, iterations=5):
    """Test DFS maze generation time complexity"""
    times = []
    for _ in range(iterations):
        generator = MazeGenerator("Custom")
        generator.rows, generator.cols = rows, cols

        start_time = time.perf_counter()
        generator.generate_maze()
        elapsed = time.perf_counter() - start_time

        times.append(elapsed)

    return sum(times) / iterations  # Return average

def test_bfs_solving(rows, cols, iterations=5):
    """Test BFS solving time complexity"""
    times = []
    for _ in range(iterations):
        # Generate a consistent maze for fair comparison
        generator = MazeGenerator("Custom")
        generator.rows, generator.cols = rows, cols
        maze = generator.generate_maze()

        display = MazeGraphDisplay(maze)

        start_time = time.perf_counter()
        display.render_maze_with_bfs_traversal(visualize=False)  # Disable GUI
        elapsed = time.perf_counter() - start_time

        times.append(elapsed)

    return sum(times) / iterations

def run_complexity_analysis(max_size=31, step=10):
    """Run tests across different maze sizes"""
    sizes = list(range(11, max_size + 1, step))  # [11, 21, 31]
    dfs_times = []
    bfs_times = []

    for size in sizes:
        print(f"Testing {size}x{size} maze...")
        dfs_times.append(test_dfs_generation(size, size))
        bfs_times.append(test_bfs_solving(size, size))

    return sizes, dfs_times, bfs_times

def plot_results(sizes, dfs_times, bfs_times):
    """Visualize time complexity results"""
    plt.figure(figsize=(12, 6))

    # Plot DFS Generation
    plt.subplot(1, 2, 1)
    plt.plot(sizes, dfs_times, 'o-', label='Measured')
    plt.plot(sizes, [s**2 * 1e-5 for s in sizes], '--', label='O(n²) reference')
    plt.xlabel("Maze Size (n x n)")
    plt.ylabel("Time (seconds)")
    plt.title("DFS Maze Generation\nTime Complexity")
    plt.legend()
    plt.grid(True)

    # Plot BFS Solving
    plt.subplot(1, 2, 2)
    plt.plot(sizes, bfs_times, 'o-', label='Measured')
    plt.plot(sizes, [s**2 * 3e-5 for s in sizes], '--', label='O(V+E) reference')
    plt.xlabel("Maze Size (n x n)")
    plt.ylabel("Time (seconds)")
    plt.title("BFS Maze Solving\nTime Complexity")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("maze_performance.png")
    plt.show()

if __name__ == "__main__":
    sizes, dfs_times, bfs_times = run_complexity_analysis()
    print("DFS Times:", dfs_times)
    print("BFS Times:", bfs_times)
    plot_results(sizes, dfs_times, bfs_times)