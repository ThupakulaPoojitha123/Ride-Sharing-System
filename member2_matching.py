# -*- coding: utf-8 -*-
"""Member 2: Matching Server - Nearest driver matching"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from shared_utils import save_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared_utils import save_data

import heapq
import math

class DriverMatcher:
    def __init__(self):
        self.drivers = []
    
    def add_driver(self, driver_id, lat, lon):
        self.drivers.append({'id': driver_id, 'lat': lat, 'lon': lon, 'available': True})
    
    def distance(self, lat1, lon1, lat2, lon2):
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    
    def find_nearest(self, rider_lat, rider_lon, top_k=3):
        heap = []
        for driver in self.drivers:
            if driver['available']:
                dist = self.distance(rider_lat, rider_lon, driver['lat'], driver['lon'])
                heapq.heappush(heap, (dist, driver['id'], driver['lat'], driver['lon']))
        
        matches = []
        for _ in range(min(top_k, len(heap))):
            if heap:
                dist, driver_id, lat, lon = heapq.heappop(heap)
                matches.append({'driver_id': driver_id, 'distance': dist, 'lat': lat, 'lon': lon})
        
        return matches

if __name__ == "__main__":
    print("=" * 50)
    print("   MEMBER 2: DRIVER MATCHING SERVER")
    print("=" * 50)
    
    matcher = DriverMatcher()
    
    # Add sample drivers
    print("\nAdding drivers to the system...")
    sample_drivers = [
        ('D1', 10.5, 20.3),
        ('D2', 15.2, 25.8),
        ('D3', 12.0, 22.5),
        ('D4', 11.5, 21.0),
        ('D5', 14.0, 24.0),
    ]
    
    for driver_id, lat, lon in sample_drivers:
        matcher.add_driver(driver_id, lat, lon)
        print(f"  Driver {driver_id} at ({lat}, {lon})")
    
    print(f"\n{len(matcher.drivers)} drivers online")
    
    while True:
        print("\n" + "=" * 50)
        rider_input = input("Enter rider location (lat lon) or 'quit': ").strip()
        if rider_input.lower() == 'quit':
            break
        
        try:
            rider_lat, rider_lon = map(float, rider_input.split())
        except:
            print("ERROR: Invalid input! Use format: lat lon (e.g., 11.0 21.5)")
            continue
        
        matches = matcher.find_nearest(rider_lat, rider_lon)
        
        if matches:
            print(f"\nFound {len(matches)} nearby drivers:")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. Driver {match['driver_id']}")
                print(f"     Distance: {match['distance']:.2f} km")
                print(f"     Location: ({match['lat']}, {match['lon']})")
            
            # Save best match for pricing
            match_data = {
                'rider_location': {'lat': rider_lat, 'lon': rider_lon},
                'matched_driver': matches[0],
                'num_available_drivers': len(matcher.drivers)
            }
            save_data('match.json', match_data)
            print(f"\nMatch saved for pricing calculation")
        else:
            print("ERROR: No available drivers found!")
    
    print("\nMatching server closed.")
