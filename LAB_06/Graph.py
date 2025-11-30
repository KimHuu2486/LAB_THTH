import re
from collections import deque
import json
from collections import defaultdict
import copy

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
                
        graph.vertices = sorted(vertices_set)
        graph.build_adj_matrix()
        
        return graph
                
    @staticmethod
    def calc_weight(model: str, capacity: str, duration: str) -> float:
        seats = list(map(int, re.findall(r"\d+", capacity)))
        total_seats = sum(seats) if seats else 1
        
        s = duration.lower()
        h_match = re.search(r"(\d+)\s*hour", s)
        m_match = re.search(r"(\d+)\s*minute", s)
        
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
    
    def base_undirected_graph(self):
        if not self.directed:
            return copy.deepcopy(self)
        
        graph = Graph(directed = False)
        graph.vertices = list(self.vertices)
        seen = set()
        
        for u, neighbors in self.adj_list.items():
            for v, w in neighbors:
                a, b = sorted([u, v])
                if (a, b) in seen:
                    continue
                seen.add((a,b))
                
                graph.adj_list[a].append((b, w))
                graph.adj_list[b].append((a, w))
                
                graph.edge_list.append((a, b, w))
                
        graph.build_adj_matrix()
        
        return graph
    
    def complement_graph(self):
        # Đồ thị có hướng không bù được
        if self.directed:
            return copy.deepcopy(self)
        
        vertices = list(self.vertices)
        existing_edges = set()
        for u, neighbors in self.adj_list.items():
            for v, w in neighbors:
                a, b = sorted([u, v])
                existing_edges.add((a, b))
                
        comp_graph = Graph(directed = False)
        comp_graph.vertices = list(vertices)
        
        n = len(vertices)
        
        for i in range (n):
            for j in range (i + 1, n):
                u, v = vertices[i], vertices[j]
                a, b = sorted((u, v))
                if (a, b) not in existing_edges:
                    w = 1.0
                    comp_graph.adj_list[u].append((v, w))
                    comp_graph.adj_list[v].append((u, w))
                    
                    comp_graph.edge_list.append((u, v, w))
                    
        comp_graph.build_adj_matrix()
        return comp_graph
        

    def converse_graph(self):
        # Đồ thị vô hướng thì không đảo được
        if not self.directed:
            return copy.deepcopy(self)
        
        converse_graph = Graph(directed = True)
        converse_graph.vertices = list(self.vertices)
        
        for u, neighbors in self.adj_list.items():
            for v, w in neighbors:
                converse_graph.adj_list[v].append((u, w))
                converse_graph.edge_list.append((v, u, w))
                
        converse_graph.build_adj_matrix()
        return converse_graph
                
    
    def DFS(self, start):
        visited = set()
        order = []
        
        def go(u):
            visited.add(u)
            order.append(u)
            for v, w in self.adj_list[u]:
                if v not in visited:
                    go(v)
        
        go(start)
        return order
    

    def BFS(self, start):
        visited = {start}
        order = []
        q = deque([start])
        
        while q:
            u = q.popleft()
            order.append(u)
            for v, w in self.adj_list[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
                    
        return order
    
    
    def is_complete(self):
        if self.directed:
            return False
        
        n = len(self.vertices)
        for u in self.vertices:
            if len(self.adj_list[u]) != n -1:
                return False
        return True
    
    def is_cycle(self):
        if self.directed:
            return False

        visited = set()
        def dfs(u):
            visited.add(u)
            for v, w in self.adj_list[u]:
                if v not in visited:
                    dfs(v)
                    
        
        dfs(self.vertices[0])
        if len(visited) != len(self.vertices):
            return False

        for u in self.vertices:
            if len(self.adj_list[u]) != 2:
                return False

        return True

                    
    def is_bipartite(self):
        color = {}
        
        for start in self.vertices:
            if start not in color:
                color[start] = 0
                q = deque([start])
                while q:
                    u = q.popleft()
                    for v, w in self.adj_list[u]:
                        if v not in color:
                            color[v] = 1 - color[u]
                            q.append(v)
                        elif color[v] == color[u]:
                            return False
        
        return True
    
    def is_complete_bipartite(self):
        if self.directed:
            return False
        
        color = {}
        start = self.vertices[0]
        color[start] = 0
        q = deque([start])
        
        while q:
            u = q.popleft()
            for v, w in self.adj_list[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
                
        if len(color) != len(self.vertices):
            return False
        
        A = {u for u in self.vertices if color[u] == 1}
        B = {u for u in self.vertices if color[u] == 0}
        
        if not A or not B:
            return False
        if A & B:
            return False
        
        for u in A:
            neighbors_u = {v for v, w in self.adj_list[u]}
            if neighbors_u != B:
                return False
            
        for u in B:
            neighbors_u = {v for v, w in self.adj_list[u]}
            if neighbors_u != A:
                return False
            
        return True
            
                        
    def count_connect_components(self):
        visited = set()
        comps = 0
        
        def dfs(u):
            visited.add(u)
            for v, w in self.adj_list[u]:
                if v not in visited:
                    dfs(v)
        
        for u in self.vertices:
            if u not in visited:
                comps += 1
                dfs(u)
        
        return comps

    def articulation_points(self):
        if self.directed:
            return []
        
        comps = self.count_connect_components()
        art_Points = []
        
        def dfs(u, banned, visited):
            visited.add(u)
            for v, w in self.adj_list[u]:
                if v == banned:
                    continue
                if v not in visited:
                    dfs(v, banned, visited)
        
        for banned in self.vertices:
            visited = set([banned])
            cnt = 0
            
            for u in self.vertices:
                if u not in visited:
                    cnt += 1
                    dfs(u, banned, visited)
            
            if cnt > comps:
                art_Points.append(banned)
        
        return art_Points

    def bridges(self):
        if self.directed:
            return []
        
        comps = self.count_connect_components()
        bridge = []
        seen = set()
        
        def dfs(u, banned_x, banned_y, visited):
            visited.add(u)
            for v, w in self.adj_list[u]:
                if (u == banned_x and v == banned_y) or (u == banned_y and v == banned_x):
                    continue
                if v not in visited:
                    dfs(v, banned_x, banned_y, visited)
        
        for banned_x, banned_y in self.edge_list:
            e = tuple(sorted([banned_x, banned_y]))
            if e in seen:
                continue
            seen.add(e)
            
            visited = set()
            cnt = 0 
            
            for u in self.vertices:
                if u not in visited:
                    cnt += 1
                    dfs(u, banned_x, banned_y, visited)
            
            if cnt > comps:
                bridge.append((banned_x, banned_y))
                
        return bridge

    def euler_hierholzer(self):
        # Chỉ xét đồ thị vô hướng
        if self.directed:
            return None

        adj = {u: [v for (v, w) in self.adj_list[u]] for u in self.vertices}

        odd = [u for u in self.vertices if len(adj[u]) % 2 == 1]

        if len(odd) == 0:
            # Chu trình Euler: chọn 1 đỉnh bất kỳ có cạnh
            start = None
            for u in self.vertices:
                if adj[u]:   # có ít nhất 1 cạnh
                    start = u
                    break
            if start is None:
                return []    # đồ thị không có cạnh
        elif len(odd) == 2:
            # Đường đi Euler: bắt đầu từ 1 trong 2 đỉnh bậc lẻ
            start = odd[0]
        else:
            # Không thỏa điều kiện Euler
            return None

        # Hàm DFS dùng để kiểm tra liên thông / cầu
        def dfs(u, visited, adj_local):
            visited.add(u)
            for v in adj_local[u]:
                if v not in visited:
                    dfs(v, visited, adj_local)

        # Kiểm tra các đỉnh bậc > 0 phải nằm trong cùng 1 thành phần liên thông
        visited0 = set()
        dfs(start, visited0, adj)
        for u in self.vertices:
            if adj[u] and u not in visited0:
                return None

        stack = [start]
        path = []

        while stack:
            u = stack[-1]
            if adj[u]:
                v = adj[u].pop()
                adj[v].remove(u)
                stack.append(v)
            else:
                path.append(stack.pop())

        return path[::-1]
    
    def euler_fleury(self):
        # Chỉ xét đồ thị vô hướng
        if self.directed:
            return None

        # Tạo bản sao adjacency CHỈ chứa đỉnh (bỏ weight)
        adj = {u: [v for (v, w) in self.adj_list[u]] for u in self.vertices}

        odd = [u for u in self.vertices if len(adj[u]) % 2 == 1]

        if len(odd) == 0:
            # Chu trình Euler: chọn 1 đỉnh bất kỳ có cạnh
            start = None
            for u in self.vertices:
                if adj[u]:   # có ít nhất 1 cạnh
                    start = u
                    break
            if start is None:
                return []    # đồ thị không có cạnh
        elif len(odd) == 2:
            # Đường đi Euler: bắt đầu từ 1 trong 2 đỉnh bậc lẻ
            start = odd[0]
        else:
            # Không thỏa điều kiện Euler
            return None

        # Hàm DFS dùng để kiểm tra liên thông / cầu
        def dfs(u, visited, adj_local):
            visited.add(u)
            for v in adj_local[u]:
                if v not in visited:
                    dfs(v, visited, adj_local)

        # Kiểm tra các đỉnh bậc > 0 phải nằm trong cùng 1 thành phần liên thông
        visited0 = set()
        dfs(start, visited0, adj)
        for u in self.vertices:
            if adj[u] and u not in visited0:
                return None

        def is_bridge(u, v):
            if len(adj[u]) == 1:
                return False

            visited1 = set()
            dfs(u, visited1, adj)

            # Xóa cạnh u - v tạm thời
            adj[u].remove(v)
            adj[v].remove(u)

            # Đếm lại sau khi xóa
            visited2 = set()
            dfs(u, visited2, adj)

            # Khôi phục cạnh
            adj[u].append(v)
            adj[v].append(u)

            # Nếu số đỉnh reachable giảm -> là cầu
            return len(visited2) < len(visited1)


        # Thuật toán Fleury
        path = [start]
        u = start

        while True:
            if not adj[u]:
                break  # hết cạnh đi ra từ u

            chosen = None

            for v in adj[u]:
                if len(adj[u]) == 1:
                    chosen = v
                    break

                if not is_bridge(u, v):
                    chosen = v
                    break

            if chosen is None:
                chosen = adj[u][0]

            adj[u].remove(chosen)
            adj[chosen].remove(u)

            path.append(chosen)
            u = chosen

        return path


if __name__ == "__main__":
    
    g = Graph.load_graph_from_jl("input.jl", directed = False)
    g.print_adj_list()
    print("\n")
    # g.print_adj_matrix()
    # print("\n")
    g.print_edge_list()
