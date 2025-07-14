import sys
from memory_profiler import memory_usage
import matplotlib.pyplot as plt
from MazeMatrix import MazeGenerator
from MazeDisplay import MazeGraphDisplay

def generate_maze_dfs(rows, cols):
    """Wrapper function for DFS maze generation"""
    generator = MazeGenerator("Custom")
    generator.rows, generator.cols = rows, cols
    return generator.generate_maze()

def solve_maze_bfs(maze):
    """Wrapper function for BFS solving"""
    display = MazeGraphDisplay(maze)
    display.render_maze_with_bfs_traversal(visualize=False)

def profile_memory(func, *args, **kwargs):
    """Measure memory usage of a function"""
    # Force garbage collection first
    import gc
    gc.collect()
    
    # Profile memory with 0.1s interval
    mem_usage = memory_usage((func, args, kwargs), interval=0.1, timeout=60)
    return max(mem_usage) - min(mem_usage)  # Return peak memory delta

def run_memory_tests(max_size=31, step=10):
    """Test memory usage across different maze sizes"""
    sizes = list(range(11, max_size + 1, step))  # [11, 21, 31]
    dfs_memory = []
    bfs_memory = []
    
    for size in sizes:
        print(f"Testing {size}x{size} maze...")
        
        # Profile DFS Generation
        dfs_peak = profile_memory(generate_maze_dfs, size, size)
        dfs_memory.append(dfs_peak)
        
        # Generate maze once for BFS test
        maze = generate_maze_dfs(size, size)
        
        # Profile BFS Solving
        bfs_peak = profile_memory(solve_maze_bfs, maze)
        bfs_memory.append(bfs_peak)
    
    return sizes, dfs_memory, bfs_memory

def plot_memory_results(sizes, dfs_memory, bfs_memory):
    """Visualize memory usage results"""
    plt.figure(figsize=(12, 6))
    
    # Plot DFS Memory
    plt.subplot(1, 2, 1)
    plt.plot(sizes, dfs_memory, 'o-', label='Measured')
    plt.plot(sizes, [s**2 * 0.0005 for s in sizes], '--', label='O(n²) reference') 
    plt.xlabel("Maze Size (n x n)")
    plt.ylabel("Memory (MB)")
    plt.title("DFS Maze Generation\nMemory Usage")
    plt.legend()
    plt.grid(True)
    
    # Plot BFS Memory
    plt.subplot(1, 2, 2)
    plt.plot(sizes, bfs_memory, 'o-', label='Measured')
    plt.plot(sizes, [s**2 * 0.0003 for s in sizes], '--', label='O(n²) reference')
    plt.xlabel("Maze Size (n x n)")
    plt.ylabel("Memory (MB)")
    plt.title("BFS Maze Solving\nMemory Usage")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("maze_memory_usage.png")
    plt.show()

if __name__ == "__main__":
    # Ensure you have memory_profiler installed: pip install memory_profiler
    sizes, dfs_mem, bfs_mem = run_memory_tests()
    print("DFS Memory (MB):", dfs_mem)
    print("BFS Memory (MB):", bfs_mem)
    plot_memory_results(sizes, dfs_mem, bfs_mem)