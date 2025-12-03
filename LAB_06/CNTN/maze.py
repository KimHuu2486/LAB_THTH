import random
from collections import deque

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def generate_maze(n):
    visited = [[False] * n for _  in range (n)]
    
    def cell_to_grid(r, c):
        return r * 2 + 1, c * 2 + 1
    
    grid = [['#'] * (2 * n + 1) for _ in range (2 * n + 1)]
    
    
    def dfs(r, c):
        visited[r][c] = True
        r_grid, c_grid = cell_to_grid(r, c)
        grid[r_grid][c_grid] = " "
        
        dirs = DIRS[:]
        random.shuffle(dirs)
        
        for x, y  in dirs:
            new_r = r + x
            new_c = c + y
            if not (0 <= new_r < n and 0 <= new_c < n):
                continue
            if visited[new_r][new_c]:
                continue
            
            new_r_grid, new_c_grid = cell_to_grid(new_r, new_c)
            
            r_wall = (r_grid + new_r_grid) // 2
            c_wall = (c_grid + new_c_grid) // 2
            grid[r_wall][c_wall] = " "
            
            dfs(new_r, new_c)
            
    dfs(0, 0)
    
    grid[0][1] = " "
    grid[2 * n][2* n - 1] = " "
    
    return ["".join(row) for row in grid]

def findPath(grid):
    n = len(grid)
    sr, sc = 1, 1
    er, ec = n - 1, n - 2
    
    if grid[sr][sc] == "#" or grid[er][ec] == "#":
        return None
    
    q = deque()
    q.append((sr, sc))
    visited = [[False] * n for _ in range(n)]
    visited[sr][sc] = True
    parent = {}

    while q:
        r, c = q.popleft()
        
        if r == er and c == ec:
            path = []
            cur = (er, ec)
            while cur != (sr, sc):
                path.append(cur)
                cur = parent[cur]
            path.append((sr, sc))
            path.reverse()
            return path
        
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == " " and not visited[nr][nc]:
                    q.append((nr, nc))
                    visited[nr][nc] = True
                    parent[(nr, nc)] = (r, c)
    
    return None
                    

if __name__ == "__main__":
    n = int(input())

    maze = generate_maze(n)
    with open("maze.txt", "w", encoding = "utf-8") as fw:
        for line in maze:
            fw.write(line + "\n")
            
    
    grid = []
    with open("maze.txt", "r", encoding = "utf-8") as fr:
        for line in fr:
            grid.append(list(line.rstrip("\n")))
    
    path = findPath(grid)
    with open("path.txt", "w", encoding = "utf-8") as fw:
        if path is None:
            fw.write("Không có đường đi\n")
        else:
            for cur in path:
                fw.write(f"{cur} -> ")