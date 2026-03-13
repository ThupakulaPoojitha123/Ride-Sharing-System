# -*- coding: utf-8 -*-
"""Member 1: Routing Server - Dijkstra's shortest path"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from shared_utils import save_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared_utils import save_data

import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
    
    def add_edge(self, u, v, weight):
        self.edges[u].append((v, weight))
        self.edges[v].append((u, weight))
    
    def dijkstra(self, start, end):
        heap = [(0, start, [])]
        visited = set()
        
        while heap:
            cost, node, path = heapq.heappop(heap)
            if node in visited:
                continue
            path = path + [node]
            if node == end:
                return cost, path
            visited.add(node)
            for neighbor, weight in self.edges[node]:
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + weight, neighbor, path))
        return float('inf'), []

if __name__ == "__main__":
    print("=" * 50)
    print("   MEMBER 1: ROUTING SERVER")
    print("=" * 50)
    
    g = Graph()
    
    # Pre-populate sample road network
    print("\nBuilding road network...")
    roads = [
        ('A', 'B', 5), ('A', 'C', 3), ('B', 'C', 2),
        ('B', 'D', 6), ('C', 'D', 7), ('C', 'E', 4),
        ('D', 'E', 2), ('D', 'F', 3), ('E', 'F', 5)
    ]
    
    for u, v, w in roads:
        g.add_edge(u, v, w)
        print(f"  Road: {u} <-> {v} (Distance: {w} km)")
    
    print("\nAvailable locations: A, B, C, D, E, F")
    
    while True:
        print("\n" + "=" * 50)
        start = input("Enter start location (or 'quit'): ").strip().upper()
        if start == 'QUIT':
            break
        
        end = input("Enter end location: ").strip().upper()
        
        if start not in g.edges or end not in g.edges:
            print("ERROR: Invalid location!")
            continue
        
        cost, path = g.dijkstra(start, end)
        
        if path:
            route_data = {
                'start': start,
                'end': end,
                'distance': cost,
                'path': path
            }
            save_data('route.json', route_data)
            
            print(f"\nShortest Route Found:")
            print(f"   Path: {' -> '.join(path)}")
            print(f"   Distance: {cost} km")
            print(f"Route saved for pricing calculation")
        else:
            print("ERROR: No route found!")
    
    print("\nRouting server closed.")
