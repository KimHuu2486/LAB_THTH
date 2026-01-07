from collections import deque
import re
import heapq

def load_from_file(filename: str) -> dict:
    adj = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(':')
                source = int(parts[0].strip())
                
                connections = re.findall(r'\((\d+),\s*(\d+)\)', parts[1])
                
                for target, weight in connections:
                    if int(source) not in adj:
                        adj[int(source)] = []
                    adj[int(source)].append((int(target), int(weight)))
                    
    return adj

class Graph:
    def __init__(self, filename, directed = True) -> None:
        self.adj = load_from_file(filename)
        self.directed = directed
        self.vertices = set()
        self.edges = []
        
        for u, neighbor in self.adj.items():
            self.vertices.add(u)
            for v, w in neighbor:
                self.vertices.add(v)
                self.edges.append((u, v, w))
        
    def print_adj(self) -> None:
        for node in sorted(self.adj.keys()):
            print(f"{node}: {self.adj[node]}")
            
    def calculate_vertices(self) -> int:
        return len(self.vertices)

    def calculate_edges(self) -> int:
        return len(self.edges)
    
    def calculate_degree(self, node: int) -> int:
        if node not in self.adj:
            return 0
        
        if self.directed:
            out_degree = len(self.adj[node])
            in_degree = 0
            for u in self.adj:
                for v, _ in self.adj[u]:
                    if v == node:
                        in_degree += 1
                    
            return in_degree, out_degree
            
        return len(self.adj[node])
    
    def dfs(self, start) -> list:
        visited = set()
        result = []
        
        def dfs_helper(node):
            visited.add(node)
            result.append(node)
            
            for neighbor, _ in self.adj.get(node, []):
                if neighbor not in visited:
                    dfs_helper(neighbor)
                    
        dfs_helper(start)
        return result
    
    def bfs(self, start) -> list:
        visited = set()
        result = []
        queue = deque([start])
        visited.add(start)
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor, _ in self.adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        return result
    
    def count_connected_components(self) -> int:
        visited = set()
        components = 0
        
        for node in self.vertices:
            if node not in visited:
                components += 1
                
                def dfs_helper(node):
                    visited.add(node)
                    for neighbor, _ in self.adj.get(node, []):
                        if neighbor not in visited:
                            dfs_helper(neighbor)
                                
                dfs_helper(node)
                
        return components

    def bfs_shortest_path(self, start, end) -> list:
        visited = set()
        queue = deque([start])
        visited.add(start)
        parent = {start: None}
        
        while queue:
            current_node = queue.popleft()
            
            if current_node == end:
                break
            
            for neighbor, _ in self.adj.get(current_node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_node
                    queue.append(neighbor)
                    
        if end not in parent:
            return None
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def dijkstra(self, start, end):
        pq = [(0, start, [start])]
        visited = set()
        min_dist = {v: float('inf') for v in self.vertices}
        min_dist[start] = 0
        
        while pq:
            curr_dist, node, path = heapq.heappop(pq)
            
            if node in visited:
                continue
            visited.add(node)
            
            if node == end:
                return curr_dist, path
            
            for neighbor, weight in self.adj.get(node, []):
                if neighbor not in visited:
                    new_dist = curr_dist + weight
                    if new_dist < min_dist[neighbor]:
                        min_dist[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))
                        
        return float('inf'), []

    def base_undirected(self):
        undirected_adj = {}
        undirected_edges = set()
        
        for u in self.adj:
            for v, w in self.adj[u]:
                if u not in undirected_adj:
                    undirected_adj[u] = []
                if v not in undirected_adj:
                    undirected_adj[v] = []
                undirected_adj[u].append((v, w))
                undirected_adj[v].append((u, w))
                undirected_edges.add((min(u, v), max(u, v), w))
                
        self.adj = undirected_adj
        self.edges = list(undirected_edges)
        self.directed = False

if __name__ == "__main__":
    filename = 'graph.txt'
    graph = Graph(filename)
    graph.print_adj()
    
    print(graph.dijkstra(1, 5))