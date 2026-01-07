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

    def prim_mst(self, start_node) -> list:
        if not self.directed:
            mst_edges = []
            mst_weight = 0
            visited = set()
            min_heap = []            
            visited.add(start_node)
            
            for neighbor, weight in self.adj.get(start_node, []):
                heapq.heappush(min_heap, (weight, start_node, neighbor))
                
            while min_heap and len(visited) < len(self.vertices):
                weight, u, v = heapq.heappop(min_heap)
                if v not in visited:
                    visited.add(v)
                    mst_edges.append((u, v, weight))
                    mst_weight += weight
                    
                    for next_neighbor, next_weight in self.adj.get(v, []):
                        if next_neighbor not in visited:
                            heapq.heappush(min_heap, (next_weight, v, next_neighbor))
                            
            return mst_edges, mst_weight
        
        else:
            return None
        
    def kruskal_mst(self) -> list:
        if not self.directed:
            sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
            mst = []
            mst_weight = 0

            parent = {v: v for v in self.vertices}

            def find_root(v):
                if parent[v] == v:
                    return v
                parent[v] = find_root(parent[v])
                return parent[v]

            def union(root_u, root_v):
                parent[root_u] = root_v

            for u, v, w in sorted_edges:
                root_u = find_root(u)
                root_v = find_root(v)

                if root_u != root_v:
                    union(root_u, root_v)
                    mst.append((u, v, w))
                    mst_weight += w
                    
            return mst, mst_weight
        
        else:
            return None

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
    
    graph.base_undirected()
    print(graph.prim_mst(1))
    print(graph.kruskal_mst())