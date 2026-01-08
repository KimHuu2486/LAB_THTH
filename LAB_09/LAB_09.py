from collections import deque
import re

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

    def edmond_karp(self, source, sink):
        
        max_node = max(self.vertices)
        capacity = [[0] * (max_node + 1) for _ in range(max_node + 1)]
        
        # Tạo đồ thị thặng dư
        for u in self.adj:
            for v, w in self.adj[u]:
                capacity[u][v] = w

        max_flow = 0
        parent = [-1] * (max_node + 1)

        # Tìm đường tăng luồng
        def bfs():
            fill_parent = [-1] * (max_node + 1)
            queue = deque([source])
            fill_parent[source] = source
            
            while queue:
                u = queue.popleft()
                
                for v in range(max_node + 1):
                    if fill_parent[v] == -1 and capacity[u][v] > 0:
                        fill_parent[v] = u
                        if v == sink:
                            return fill_parent
                        queue.append(v)
            return None

        while True:
            parent = bfs()
            if not parent:
                break
                
            path_flow = float('inf')
            s = sink
            while s != source:
                u = parent[s]
                path_flow = min(path_flow, capacity[u][s])
                s = u
            
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                capacity[u][v] -= path_flow
                capacity[v][u] += path_flow
                v = u
                
        return max_flow, capacity

    def ford_fulkerson(self, source, sink):
        max_node = max(self.vertices) if self.vertices else 0
        capacity = [[0] * (max_node + 1) for _ in range(max_node + 1)]
        
        # Tạo đồ thị thặng dư
        for u in self.adj:
            for v, w in self.adj[u]:
                capacity[u][v] = w

        max_flow = 0
        parent = [-1] * (max_node + 1)

        # Tìm đường tăng luồng
        def dfs():
            fill_parent = [-1] * (max_node + 1)
            stack = [source]
            fill_parent[source] = source
            
            while stack:
                u = stack.pop()
                
                if u == sink:
                    return fill_parent
                
                for v in range(max_node + 1):
                    if fill_parent[v] == -1 and capacity[u][v] > 0:
                        fill_parent[v] = u
                        stack.append(v)
            return None

        # Nếu vẫn còn đường tăng luồng
        while True:
            parent = dfs()
            if not parent:
                break
                
            path_flow = float('inf')
            s = sink
            while s != source:
                u = parent[s]
                path_flow = min(path_flow, capacity[u][s])
                s = u
            
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                capacity[u][v] -= path_flow
                capacity[v][u] += path_flow
                v = u
                
        return max_flow, capacity
    
    def get_min_cut_from_residual(self, source, residual_capacity):
        max_node = len(residual_capacity) - 1
        visited_S = set()
        
        queue = deque([source])
        visited_S.add(source)
        while queue:
            u = queue.popleft()
            for v in range(max_node + 1):
                if v not in visited_S and residual_capacity[u][v] > 0:
                    visited_S.add(v)
                    queue.append(v)
        
        min_cut_edges = []
        min_cut_value = 0
        for u in self.adj:
            for v, w in self.adj[u]:
                if u in visited_S and v not in visited_S:
                    min_cut_edges.append((u, v, w))
                    min_cut_value += w
        return min_cut_edges, min_cut_value

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
    
    source, sink = 2, 8
    print(source, sink)
    max_flow, residual_graph = graph.edmond_karp(source, sink)
    print(f"Max Flow: {max_flow}")
    max_flow, residual_graph = graph.ford_fulkerson(source, sink)
    print(f"Max Flow: {max_flow}")
    
    
    # Bây giờ mới gọi được min-cut
    cut_edges, cut_val = graph.get_min_cut_from_residual(source, residual_graph)
    print(f"Min Cut Value: {cut_val}")
    print(f"Min Cut Edges: {cut_edges}")
    
    
