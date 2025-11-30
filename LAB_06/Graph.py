import re
from collections import deque
import json
from collections import defaultdict

class Graph:
    def __init__(self, directed = False):
        self.directed = directed
        self.adj_list = defaultdict(list)
        self.vertices = []
        self.adj_matrix = []
        self.edge_list = []

    @classmethod
    def load_graph_from_jl(cls, pathFile, directed = False):
        graph = cls(directed)
        vertices_set = set()
        
        with open(pathFile, "r", encoding = "utf-8") as f:
            for line in f:
                line  = line.strip()
                if not line:
                    continue
                
                obj = json.loads(line)
                (pair, info), = obj.items()
                
                u_raws, v_raws = pair.split(",", 1)
                u = u_raws.strip()
                v = v_raws.strip()
                
                model, capacity, duration = info
                
                weight = cls.calc_weight(model, capacity, duration)
                
                graph.adj_list[u].append((v, weight))
                
                if not directed:
                    graph.adj_list[v].append((u, weight))
                    
                if directed:
                    graph.edge_list.append((u, v, weight))
                
                else:
                    a, b = sorted([u, v])
                    graph.edge_list.append((a, b, weight))
                    
                vertices_set.add(u)
                vertices_set.add(v)
                
        graph.vertices = list(vertices_set)
        graph.build_adj_matrix()
        
        return graph
                
    @staticmethod
    def calc_weight(model: str, capacity: str, duration: str) -> float:
        seats = list(map(int, re.findall(r"\d+", capacity)))
        total_seats = sum(seats)
        
        s = duration.lower()
        h_match = re.search(r"(\d+)\s*hours", s)
        m_match = re.search(r"(\d+)\s*minutes", s)
        
        hours = int(h_match.group(1)) if h_match else 0
        minutes = int(m_match.group(1)) if m_match else 0
        
        total_minutes = hours * 60 + minutes
        
        return total_minutes / total_seats
    
    def build_adj_matrix(self):
        n = len(self.vertices)

        self.adj_matrix = [[None for _ in range(n)] for _ in range(n)]
        
        index = {v: i for i, v in enumerate(self.vertices)}
        
        for u, neighbors in self.adj_list.items():
            i = index[u]
            for v, weight in neighbors:
                j = index[v]
                self.adj_matrix[i][j] = weight

    def print_adj_list(self):
        print("Danh sach ke: ")
        for u in self.vertices:
            print(f"{u}:")
            for v, w in self.adj_list.get(u, []):
                print(f"  -> {v}: {w:.2f}")

    def print_adj_matrix(self):
        n = len(self.vertices)

        print("Ma trận kề (trọng số, '∞' nếu không có cạnh):")

        # In header cột (tên đỉnh)
        header = " " * 8 + " ".join(f"{v:>12}" for v in self.vertices)
        print(header)

        # In từng dòng
        for i, row in enumerate(self.adj_matrix):
            # tên đỉnh đầu dòng
            line = f"{self.vertices[i]:>8}"
            for cell in row:
                if cell is None:
                    line += f"{'∞':>12}"
                else:
                    # cell là float (weight) -> in 2 chữ số thập phân
                    line += f"{cell:>12.2f}"
            print(line)

    def print_edge_list(self):
        print("Danh sách cạnh:")
        for u, v, w in self.edge_list:
            print(f"({u}, {v})  w = {w:.2f}")

    def isDirected(self):
        return self.directed
    
    def countEdges(self):
        return len(self.edge_list)
    
    def countVertices(self):
        return len(self.vertices)
    
    def Degree(self, u):
        if self.directed:
            out_deg = len(self.adj_list.get(u, []))
            in_deg = 0
            for src, neighbors in self.adj_list.items():
                for v, _ in neighbors:
                    if v == u:
                        in_deg += 1
            return in_deg, out_deg
        else :
            return len(self.adj_list.get(u, []))
    
    def isolated_vertices(self):
        isolated = []
        for  u in self.vertices:
            deg = self.Degree(u)

            if self.directed:
                in_deg, out_deg = deg
                if in_deg == 0 and out_deg == 0:
                    isolated.append(u)
            else:
                if deg == 0:
                    isolated.append(u)
        return isolated 
    
    def leaf_vertices(self):
        leaf = []
        for u in self.vertices:
            deg = self.Degree(u)

            if self.directed:
                in_deg, out_deg = deg
                if in_deg + out_deg == 1:
                    leaf.append(u)
            else:
                if deg == 1:
                    leaf.append(u)
        return leaf
    
    # def to_undirected(self):
    #     g2 = Graph(directed = False)
    #     for u in self.vertices:
    #         for v in self.adj_list[u]:
    #             g2.adj_list.setdefault(u, [])
    #             g2.adj_list[u].append(v)
    #             g2.adj_list.setdefault(v, [])
    #             if u not in g2.adj_list[v]:
    #                 g2.adj_list[v].append(u)
        
    #     g2.vertices = g2.adj_list.keys()
    #     g2.build_adj_matrix()
    #     g2.build_edge_list()
    #     return g2
    
    # def complement_graph(self):
    #     comp = Graph(directed = self.directed)
    #     V = self.vertices

    #     neighbor_sets = {u: set(self.adj_list.get(u, [])) for u in V}

    #     comp.adj_list = {u : [v for v in V if v != u and v not in neighbor_sets[u]] for u in V}

    #     comp.vertices = V[:]
    #     return comp

    # def converse_graph(self):
    #     if not self.directed:
    #         return self.copy()
        
    #     g2 = Graph(directed = True)
    #     g2.adj_list = {u: [] for u in self.vertices}
        
    #     for u in self.vertices:
    #         for v in self.adj_list[u]:
    #             g2.adj_list[v].append(u)
                
    #     g2.vertices = self.vertices[:]
    #     return g2        
    
    # def DFS(self, start):
    #     visited = set()
    #     order = []
        
    #     def go(u):
    #         visited.add(u)
    #         order.append(u)
    #         for v in self.adj_list[u]:
    #             if v not in visited:
    #                 go(v)
        
    #     go(start)
    #     return order
    

    # def BFS(self, start):
    #     visited = {start}
    #     q = deque([start])
    #     order = []
        
    #     while q:
    #         u = q.popleft()
    #         order.append(u)
    #         for v in self.adj_list[u]:
    #             if v not in visited:
    #                 visited.add(v)
    #                 q.append(v)
        
    #     return order
    
    # def is_complete(self):
    #     if self.directed:
    #         return False
        
    #     n = len(self.vertices)
    #     for u in self.vertices:
    #         if len(self.adj_list[u]) != n -1:
    #             return False
    #     return True
    
    # def is_cycle(self):
    #     for u in self.vertices:
    #         if len(self.adj_list[u]) != 2:
    #             return False
        
    #     visited = set()
        
    #     def dfs(start):
    #         visited.add(start)
    #         for v in self.adj_list[start]:
    #             if v not in visited:
    #                 dfs(v)
        
    #     dfs(self.vertices[0])
        
    #     return len(visited) == len(self.vertices)
                    
    # def is_bipartite(self):
    #     color = {}
        
    #     for start in self.vertices:
    #         if start not in color:
    #             color[start] = 0
    #             q = deque([start])
    #             while q:
    #                 u = q.popleft()
    #                 for v in self.adj_list[u]:
    #                     if v not in color:
    #                         color[v] = 1 - color[u]
    #                         q.append(v)
    #                     elif color[v] == color[u]:
    #                         return False
        
    #     return True
    
    # def is_complete_bipartite(self):
    #     if self.directed:
    #         return False
        
    #     color = {}
        
    #     start = self.vertices[0]
    #     color[start] = 0
    #     q = deque([start])
        
    #     while (q):
    #         u  = q.popleft()
    #         for v in self.adj_list[u]:
    #             if v not in color:
    #                 color[v] = 1 - color[u]
    #                 q.append(v)
    #             elif color[v] == color[u]:
    #                 return False
                
    #     if (len(color) != len(self.vertices)):
    #         return False
        
    #     A = [u for u in self.vertices if color[u] == 0]
    #     B = [u for u in self.vertices if color[u] == 1]
        
    #     for u in A:
    #         if set(self.adj_list[u]) != set(B):
    #             return False
            
    #     for v in B:
    #         if set(self.adj_list[v]) != set(A):
    #             return False       
        
    #     return True
                        
    # def count_connect_components(self):
    #     visited = set()
    #     comps = 0
        
    #     def dfs(u):
    #         visited.add(u)
    #         for v in self.adj_list[u]:
    #             if v not in visited:
    #                 dfs(v)
        
    #     for u in self.vertices:
    #         if u not in visited:
    #             comps += 1
    #             dfs(u)
        
    #     return comps

    # def articulation_points(self):
    #     comps = self.count_connect_components()
    #     articulationPoints = []
        
    #     def dfs(u, banned, visited):
    #         visited.add(u)
    #         for v in self.adj_list[u]:
    #             if v == banned:
    #                 continue
    #             if v not in visited:
    #                 dfs(v, banned, visited)
                    
    #     for banned in self.vertices:
    #         visited = set([banned])
    #         cnt = 0
            
    #         for u in self.vertices:
    #             if u not in visited:
    #                 dfs(u, banned, visited)
    #                 cnt+=1
            
    #         if cnt > comps:
    #             articulationPoints.append(banned)
                
    #     return articulationPoints

    # def bridges(self):
    #     comps = self.count_connect_components()
    #     bridge = []
    #     seen = set()
        
    #     def dfs(u, banned_x, banned_y, visited):
    #         visited.add(u)
    #         for v in self.adj_list[u]:
    #             if (u == banned_x and v == banned_y) or (u == banned_y and v == banned_x):
    #                 continue
    #             if v not in visited:
    #                 dfs(v, banned_x, banned_y, visited)
                    
    #     for banned_x, banned_y in self.edge_list:
    #         e  = tuple(sorted((banned_x, banned_y)))
    #         if e in seen:
    #             continue
    #         seen.add(e)
            
    #         visited = set()
    #         cnt = 0
            
    #         for u in self.vertices:
    #             if u not in visited:
    #                 dfs(u, banned_x, banned_y, visited)
    #                 cnt+=1
            
    #         if cnt > comps:
    #             bridge.append([banned_x, banned_y])
                
    #     return bridge

    # def euler_hierholzer(self):
    #     adjList = {u: self.adj_list[u][:] for u in self.vertices}
        
    #     odd = [u for u in  self.vertices if len(adjList[u]) % 2 == 1]
        
    #     if len(odd) == 0:
    #         start = self.vertices[0] # Chu trình Euler
    #     elif len(odd) == 2:
    #         start = odd[0] # Đường đi Euler
    #     else:
    #         return None
            
    #     stack = [start]
    #     path = []
        
    #     while stack:
    #         u = stack[-1]
    #         if adjList[u]:
    #             v = adjList[u].pop()
    #             adjList[v].remove(u)
    #             stack.append(v)
    #         else:
    #             path.append(stack.pop())
        
    #     return path[::-1]
    
    # def euler_fleury(self):
    #     adjList = {u: self.adj_list[u][:] for u in self.vertices}
        
    #     odd = [u for u in self.vertices if len(adjList[u]) % 2 == 1]
        
    #     if len(odd) == 0:
    #         start = self.vertices[0] # chu trình euler
    #     elif len(odd) == 2:
    #         start = odd[0] # đường đi euler
    #     else:
    #         return None
        
    #     def dfs(u, visited):
    #         visited.add(u)
    #         for v in adjList[u]:
    #             if v not in visited:
    #                 dfs(v, visited)
                    
    #     visited = set()
    #     dfs(start, visited)
    #     for u in self.vertices:
    #         if len(adjList[u]) > 0 and u not in visited:
    #             return None # Các đỉnh có bậc > 0 phải liên thông
            
    #     def is_bridge(u, v):
    #         visited1 = set()
    #         dfs(u, visited)
            
    #         adjList[u].remove(v)
    #         adjList[v].remove(u)
            
    #         visited2 = set()
    #         dfs(u, visited2)
            
    #         adjList[u].insert(0, v)
    #         adjList[v].insert(0, u)
            
    #         return len(visited2) < len(visited1)
        
    #     path = [start]
    #     u = start
        
    #     while True:
    #         if not adjList[u]:
    #             break
            
    #         chosen = None
            
    #         for v in adjList[u]:
    #             if len(adjList[u]) == 1:
    #                 chosen = v
    #                 break
                
    #             if not is_bridge(u, v):
    #                 chosen = v
    #                 break
            
    #         if chosen is None:
    #             chosen = adjList[u][0]
                
    #         adjList[u].remove(chosen)
    #         adjList[chosen].remove(u)
            
    #         path.append(chosen)
    #         u = chosen

    #     return path

        

if __name__ == "__main__":
    
    g = Graph.load_graph_from_jl("input.jl", directed = False)
    g.print_adj_list()
    print("\n")
    # g.print_adj_matrix()
    # print("\n")
    g.print_edge_list()
