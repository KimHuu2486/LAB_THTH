import re
import json
from collections import deque
import heapq


def convert_to_minutes(time_str):
    h_match = re.search(r'(\d+)\s*hour', time_str)
    m_match = re.search(r'(\d+)\s*minute', time_str)
    
    hours = int(h_match.group(1)) if h_match else 0
    minutes = int(m_match.group(1)) if m_match else 0
    
    return hours * 60 + minutes

def read_undirected_graph(filename):
    adj = {}
    vertices = set()
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            obj = json.loads(line)
            route, info = next(iter(obj.items()))

            u, v = route.split(',', 1)
            u = u.strip()
            v = v.strip()
            
            time = convert_to_minutes(info[2])
            
            if u not in adj: adj[u] = {}
            if v not in adj: adj[v] = {}
                
            adj[u][v] = time
            adj[v][u] = time
            vertices.add(u)
            vertices.add(v)
    
    return vertices, adj

def print_adj(adj):
    for u in adj:
        print(f'{u}:')
        for v, w in adj[u].items():
            print(f' -> {v} : {w}')

def prim_mst(adj, start_node):
    mst_edge = []
    mst_weight = 0
    visited = set()
    visited.add(start_node)
    min_heap = []
    
    for v, w in adj[start_node].items():
        heapq.heappush(min_heap, (w, start_node, v))
        
    while min_heap:
        w, u, v = heapq.heappop(min_heap)
        if v in visited:
            continue
        visited.add(v)
        
        mst_edge.append((u, v, w))
        mst_weight += w
        
        for next_neighbor, next_weight in adj[v].items():
            if next_neighbor not in visited:
                heapq.heappush(min_heap, (next_weight, v, next_neighbor))
          
    return mst_weight, mst_edge      

def dijkstra(adj, vertices, start, end):
    visited = set()
    min_dist = {v: float('inf') for v in vertices}
    min_dist[start] = 0
    heap = [(0, start, [start])] 
    
    while heap:
        cur_dist, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        
        if node == end:
            return cur_dist, path
        
        for neighbor, weight in adj[node].items():
            if neighbor not in visited:
                new_dist = cur_dist + weight
                if new_dist < min_dist[neighbor]:
                    min_dist[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor, path + [neighbor]))
        
    return float['inf'], []   

if __name__ == '__main__':
    vertices, adj = read_undirected_graph('g1.v2.jl')
    print_adj(adj)
    
    mst_weight, mst_edge = prim_mst(adj, 'Myanmar')
    
    print(f'MST: {mst_weight}')
    print(mst_edge)
    
            
    
                   
            