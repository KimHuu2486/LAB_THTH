import json
from collections import defaultdict

def load_json(file_path):
    adj_list = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            data = json.loads(line)
            (route, info), = data.items()
            
            u_raw, v_raw = route.split(",", 1)
            u = u_raw.strip()
            v = v_raw.strip()
            
            adj_list[u].append(v)
    return adj_list

def find_path_dfs(graph, start, end):
    if start not in graph or end not in graph:
        return None
    stack = [start]
    parent = {start: None}
    visited = set()
    
    while stack:
        node = stack.pop()
        if node == end:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            print(" -> ".join(reversed(path)))
            return True
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    parent[neighbor] = node
                    stack.append(neighbor)
    return False

if __name__ == "__main__":
    file_path = 'g1.v2.jl'
    adjacency_list = load_json(file_path)
    
    # for vertex, neighbors in adjacency_list.items():
    #     print(f"{vertex}: {neighbors}")
    
    
    # vertices = set()
    
    # for u, neighbors in adjacency_list.items():
    #     vertices.add(u)
    #     for v in neighbors:
    #         vertices.add(v)
    # print(f"Tổng số đỉnh: {len(vertices)}")
    
    test_cases = [
        ("Myanmar", "South Sudan"),
        ("Italy", "Greece"),
        ("Myanmar", "Greece"), # Thử một đường gián tiếp hoặc không tồn tại
        ("Vietnam", "USA")     # Thử một đường ngẫu nhiên
    ]
    
    for start, end in test_cases:
        print(f"Đường đi từ {start} đến {end}:")
        if not find_path_dfs(adjacency_list, start, end):
            print("Không tìm thấy đường đi.")
        print()