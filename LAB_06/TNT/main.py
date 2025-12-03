from collections import deque
from collections import defaultdict
import copy

# %%
import json
import re

class FlightGraph:
    def __init__(self, file_path):
        self.vertices = []
        self.edges = []
        self.weights = []
        self.file_path = file_path
        
        self.load_data()
        
    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                data = json.loads(line)
                (route, info), = data.items()
                
                # Tách đỉnh
                u_raw, v_raw = route.split(",", 1)
                u = u_raw.strip()
                v = v_raw.strip()
                
                self.vertices.append(u)
                self.vertices.append(v)
                
                self.edges.append((u, v))
                self.weights.append(info)
                
    def check_duplicates_vertices(self):
        original_count = len(self.vertices)
        unique_vertices = sorted(list(set(self.vertices)))
        
        self.vertices = unique_vertices
        
        print(f"Original vertex count: {original_count}")
        print(f"Unique vertex count: {len(self.vertices)}")
        
    def check_duplicates_flights(self):
        seen = set()
        duplicates = []
        
        for i in range(len(self.edges)):
            u, v = self.edges[i]
            
            info = tuple(self.weights[i])
            
            flight = (u, v, info)
            
            if flight in seen:
                duplicates.append(flight)
            else:
                seen.add(flight)

        if duplicates:
            print("Duplicate flights found:")
            for flight in duplicates:
                print(flight)
        else:
            print("No duplicate flights found.")
            
    def get_flight_info(self, src, dest):
        found = False
        for i, (u, v) in enumerate(self.edges):
            if u == src and v == dest:
                info = self.weights[i]
                print("Tìm thấy: ")
                print(f"Flight from {src} to {dest}")
                print(f"Chuyến bay: {info[0]}")
                print(f"Số ghế: {info[1]}")
                print(f"Thời gian bay: {info[2]}")
                found = True
                break
        if not found:
            print(f"No flight found from {src} to {dest}.")

    def parse_time(self, duration_str):
        s= duration_str.lower()
        h_match  = re.search(r"(\d+)\s*hour", s)
        m_match  = re.search(r"(\d+)\s*minute", s)
        
        hours = int(h_match.group(1)) if h_match else 0
        minutes = int(m_match.group(1)) if m_match else 0
        
        return hours * 60 + minutes
    
    def find_longest_shortest_flight(self):
        idx_longest = -1
        idx_shortest = -1
        
        max_duration = -1
        min_duration = float('inf')
        
        for i, info in enumerate(self.weights):
            duration = info[2]
            total_minutes = self.parse_time(duration)
            
            if total_minutes > max_duration:
                max_duration = total_minutes
                idx_longest = i
            if total_minutes < min_duration:
                min_duration = total_minutes
                idx_shortest = i
                
        print("\nLongest flight:")
        u, v = self.edges[idx_longest]
        info = self.weights[idx_longest]
        print(f"From {u} to {v}")
        print(f"Flight: {info[0]}, Seats: {info[1]}, Duration: {info[2]}")
        
        print("\nShortest flight:")
        u, v = self.edges[idx_shortest]
        info = self.weights[idx_shortest]
        print(f"From {u} to {v}")
        print(f"Flight: {info[0]}, Seats: {info[1]}, Duration: {info[2]}")

    def find_flight_by_code(self, flight_code):
        for i, info in enumerate(self.weights):
            if info[0] == flight_code:
                u, v = self.edges[i]
                print(f"Flight {flight_code} found from {u} to {v}")
                return
            
        print(f"Flight {flight_code} not found.")

    # Bổ đề bắt tay: Tổng số bậc = 2 * số cạnh
    def verify_handshaking_lemma(self):
        degree = {v: 0 for v in self.vertices}
        
        for u, v in self.edges:
            degree[u] += 1
            degree[v] += 1
        
        total_degree = sum(degree.values())
        total_edges = len(self.edges)
        print(f"Total degree: {total_degree}, Total edges: {total_edges}")
        
        if total_degree == 2 * total_edges:
            print("Handshaking lemma verified.")
        else:
            print("Handshaking lemma not verified.")
    
    def print_degrees(self):
        deg_in = {v: 0 for v in self.vertices}
        deg_out = {v: 0 for v in self.vertices}
        
        for u, v in self.edges:
            deg_out[u] += 1
            deg_in[v] += 1
        
        for v in self.vertices:
            print(f"Vertex: {v}, In-degree: {deg_in[v]}, Out-degree: {deg_out[v]}")
    
    def is_valid_walk(self, path_list):
        for i in range(len(path_list) - 1):
            u = path_list[i]
            v = path_list[i + 1]
            if (u, v) not in self.edges:
                print(f"Invalid walk: No edge from {u} to {v}")
                return False
        print("Valid walk.")
        return True
    
    # Không có cạnh trùng
    def is_valid_trail(self, path_list):
        path_edges = []
        for i in range(len(path_list) - 1):
            u = path_list[i]
            v = path_list[i + 1]
            if (u, v) not in self.edges:
                print(f"Invalid trail: No edge from {u} to {v}")
                return False
            if (u, v) in path_edges:
                print(f"Invalid trail: Edge from {u} to {v} is repeated")
                return False
            path_edges.append((u, v))
        
        print("Valid trail.")
        return True
    
    # Không có đỉnh trùng
    def is_valid_path(self, path_list):
        if not self.is_valid_trail(path_list):
            print("Invalid path: Not a valid trail")
            return False
        if len(path_list) != len(set(path_list)):
            print("Invalid path: Vertex repeated")
            return False
        print("Valid path.")
        return True
    
    def is_valid_closed_walk(self, path_list):
        if not self.is_valid_walk(path_list):
            print("Invalid closed walk: Not a valid walk")
            return False
        if path_list[0] != path_list[-1]:
            print("Invalid closed walk: Start and end vertices differ")
            return False
        print("Valid closed walk.")
        return True
    
    # Không có cạnh trùng
    def is_valid_cycle(self, path_list):
        if not self.is_valid_closed_walk(path_list):
            print("Invalid cycle: Not a valid closed walk")
            return False
            
        edges_in_path = []
        for i in range(len(path_list) - 1):
            edge = (path_list[i], path_list[i+1])
            edges_in_path.append(edge)
            
        if len(edges_in_path) != len(set(edges_in_path)):
            print("Invalid cycle: Edge repeated in cycle")
            return False
            
        print("Valid cycle.")
        return True
    
    # Không có đỉnh trùng
    def is_valid_simple_cycle(self, path_list):
        if not self.is_valid_cycle(path_list):
            print("Invalid simple cycle: Not a valid cycle")
            return False
        if len(path_list) - 1 != len(set(path_list[:-1])):
            print("Invalid simple cycle: Vertex repeated in simple cycle")
            return False
        print("Valid simple cycle.")
        return True
    
    def is_subgraph(self, other_graph):
        for u, v in self.edges:
            if (u, v) not in other_graph.edges:
                print(f"Not a subgraph: Edge from {u} to {v} not in other graph")
                return False
        print("Is a subgraph.")
        return True
    
if __name__ == "__main__":
    g = FlightGraph("g1.v2.jl")
    g.check_duplicates_vertices()  
    g.check_duplicates_flights() 
    
    g.get_flight_info("Myanmar", "South Sudan")
    g.get_flight_info("Faeroe Islands", "Ethiopia")
    
    g.find_longest_shortest_flight()
    
    print("\n")
    g.find_flight_by_code("Boeing 737-100")
    
    print("\n")
    g.verify_handshaking_lemma()
    
    # print("\nDegrees of vertices:")
    # g.print_degrees()
    
    sample_path = ["Myanmar", "South Sudan", "Saint Pierre Miquelon"] 
    print("\nChecking if the sample path is a valid walk and trail:")
    g.is_valid_walk(sample_path)
    g.is_valid_trail(sample_path)
    
    g_other = FlightGraph("input.jl")
    print("\nChecking if g_other is a subgraph of g:")
    g_other.is_subgraph(g)
# %%
