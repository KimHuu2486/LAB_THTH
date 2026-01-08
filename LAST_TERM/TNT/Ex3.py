import re
import json
from collections import deque
import heapq

def compute_seats(seats_str):
    bus_match = re.search(r'(\d+)\s*bus', seats_str)
    eco_match = re.search(r'(\d+)\s*eco', seats_str)
    
    bus = int(bus_match.group(1)) if bus_match else 0
    eco = int(eco_match.group(1)) if eco_match else 0
    
    return bus + eco

def read_directed_graph(filename, start_line, end_line):
    adj = {}
    vertices = set()
    
    with open(filename, 'r', encoding='utf-8') as f:
        cnt = 0
        for line in f:
            if not line.strip():
                continue
            
            cnt += 1
            if not (start_line <= cnt <= end_line):
                continue
            
            obj = json.loads(line)
            route, info = next(iter(obj.items()))
            u, v = route.split(',')
            u = u.strip()
            v= v.strip()
            
            seats = compute_seats(info[1])
            
            if u not in adj:
                adj[u] = {}
            if v not in adj:
                adj[v] = {}
            adj[u][v] = seats
            vertices.add(u)    
            vertices.add(v)    
            
    return vertices, adj

def print_adj(adj):
    for u in adj:
        print(f'{u}:')
        for v, w in adj[u].items():
            print(f' -> {v} : {w}')
            
def BFS(adj, source, dest):
    visited = set()
    parent = {}
    parent[source] = None
    queue = deque([source])
    visited.add(source)
    
    while queue:
        u = queue.popleft()
        if u == dest:
            break
        
        for v in adj.get(u, {}):
            if v not in visited:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                
    if dest not in parent:
        return None
    
    result = []
    node = dest
    while node is not None:
        result.append(node)
        node = parent[node]
    result.reverse()
    return result
            
def build_residual(adj):
    residual = {}
    for u in adj:
        if u not in residual:
            residual[u] = {}
        for v, c in adj[u].items():
            if v not in residual:
                residual[v] = {}
            residual[u][v] = residual[u].get(v, 0) + c
            
            residual[v].setdefault(u, residual[v].get(u, 0))
    return residual

def bfs_argumenting_path(residual, source, dest):
    parent = {source: None}
    q = deque([source])
    
    while q and dest not in parent:
        u = q.popleft()
        for v, cap_uv in residual.get(u, {}).items():
            if cap_uv > 0 and v not in parent:
                parent[v] = u
                q.append(v)
                
    if dest not in parent:
        return None, 0
    
    bottle_neck = float('inf')
    v = dest 
    while v != source:
        u = parent[v]
        bottle_neck = min(bottle_neck, residual[u][v])
        v = u
    
    return parent, bottle_neck

def edmonds_karp(adj, source, dest):
    residual = build_residual(adj)
    max_flow = 0
    
    while True:
        parent, path_flow = bfs_argumenting_path(residual, source, dest)
        if parent is None:
            break
        v = dest
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] = residual[v].get(u, 0) + path_flow
            v = u
            
        max_flow += path_flow
        
    return max_flow, residual

def find_min_cut(adj, residual, source):
    visited = set()
    q = deque([source])
    visited.add(source)
    
    while q:
        u = q.popleft()
        for v, cap_uv in residual.get(u, {}).items():
            if cap_uv > 0 and v not in visited:
                visited.add(v)
                q.append(v)
                
    min_cut_edges = []
    cut_value = 0
    for u in visited:
        for v, cap_uv in adj.get(u, {}).items():
            if v not in visited:
                min_cut_edges.append((u, v, cap_uv))
                cut_value += cap_uv
                
    return min_cut_edges, cut_value    
        
if __name__ == '__main__':
    vertices, adj = read_directed_graph('test.jl', 1, 500)
    print_adj(adj)
    
    s = 'Italy'
    t = 'Syria'

    path = BFS(adj, s, t)
    if path is None:
        print("Không có lộ trình BFS:", s, "->", t)
    else:
        print("Một đường đi BFS:", " -> ".join(path))

    max_flow, residual = edmonds_karp(adj, s, t)
    if max_flow == 0:
        print("Max Flow: 0")
        print("Không có lộ trình từ Source đến Sink (trên đồ thị có hướng).")
    else:
        print("Max Flow:", max_flow)

        cut_edges, cut_val = find_min_cut(adj, residual, s)
        print("Min Cut Value:", cut_val)
        print("Min Cut Edges:")
        for u, v, w in cut_edges:
            print(f"{u} -> {v}({w})")