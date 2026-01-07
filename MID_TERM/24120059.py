import json
import re
import itertools
from collections import deque
from typing import List, Tuple

def readfile(filename: str) -> dict:
    result = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip(): 
                continue
            
            entry = json.loads(line)
            result.update(entry)
    return result

class FGraph:
    def __init__(self, Flights: dict) -> None:
        self.adj = {}
        
        Ct = 275
        Cc = 35
        
        for route, info in Flights.items():
            flights_name = info[0]
            seat_info_str = info[1]
            time_info_str = info[2]
            
            has_digits = bool(re.search(r'\d', flights_name))
            has_hyphen = '-' in flights_name
            
            if not (has_digits and has_hyphen):
                continue
            
            u, v = route.split(',', 1)
            u, v = u.strip(), v.strip()

            bus_match = re.search(r'(\d+)\s*bus', seat_info_str)
            eco_match = re.search(r'(\d+)\s*eco', seat_info_str)
            n_bus = int(bus_match.group(1)) if bus_match else 0
            n_eco = int(eco_match.group(1)) if eco_match else 0
            total_seats = n_bus + n_eco

            h_match = re.search(r'(\d+)\s*h', time_info_str)
            m_match = re.search(r'(\d+)\s*m', time_info_str)
            hours = int(h_match.group(1)) if h_match else 0
            minutes = int(m_match.group(1)) if m_match else 0
            total_time = hours * 60 + minutes

            denominator = 3 * n_bus + n_eco
            if denominator == 0:
                ticket_price = 0
            else:
                numerator = (Ct * total_time) + (Cc * total_seats)
                ticket_price = numerator / denominator

            self.add_edge(u, v, ticket_price)
            self.add_edge(v, u, ticket_price)
        
    def add_edge(self, u, v, w):
        if u not in self.adj:
            self.adj[u] = {}
        self.adj[u][v] = w

    def print_adj_list(self):
        for u in self.adj:
            print(f"{u}:")
            for v, w in self.adj[u].items():
                print(f"  -> {v}: {w:.2f}")

    def findDirectFlights(self, country_name: str) -> List[str]:
        if country_name in self.adj:
            return list(self.adj[country_name].keys())
        else:
            return []
   
    
def is_bipartite(sub_nodes: list, graph_adj: dict) -> bool:
    color = {}
    
    for node in sub_nodes:
        if node not in color:
            queue = deque([node])
            color[node] = 0
            while queue:
                u = queue.popleft()
                neighbors = [v for v in graph_adj.get(u, {}) if v in sub_nodes]
                
                for v in neighbors:
                    if v not in color:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
    return True

def find4Bipartite(G, country_name: str) -> list[str]:
    all_countries = list(G.adj.keys())
    
    if country_name not in all_countries:
        candidates = [c for c in all_countries if c != country_name]
    else:
        return []
    
    for combo in itertools.combinations(candidates, 4):
        sub_nodes = list(combo) + [country_name]
        if is_bipartite(sub_nodes, G.adj):
            return list(combo)
    return []
                    
    
def findBST(n: int) -> int:
    if n < 0:
        return 0
    if n == 0 or n == 1:
        return 1
    
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    
    for i in range(2, n + 1):
        for j in range(i):
            dp[i] += dp[j] * dp[i - 1 - j]

    return dp[n]



if __name__ == '__main__':
    flights_data = readfile('g1.v2.jl')
    # print(flights_data)

    Graph = FGraph(flights_data)
    # Graph.print_adj_list()

    DirectFlights = Graph.findDirectFlights("Myanmar")
    print(DirectFlights)

    BipartiteCountries = find4Bipartite(Graph, "Myanmar")
    print(BipartiteCountries)
    
    print(findBST(5))