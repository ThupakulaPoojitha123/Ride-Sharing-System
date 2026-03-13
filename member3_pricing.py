# -*- coding: utf-8 -*-
"""Member 3: Pricing Client - Calculates price using route and match data"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from shared_utils import load_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared_utils import load_data

class PricingEngine:
    def __init__(self, base_rate=2.0, per_km=1.5):
        self.base_rate = base_rate
        self.per_km = per_km
    
    def calculate_price(self, distance, demand_multiplier=1.0):
        base_price = self.base_rate + (distance * self.per_km)
        surge_price = base_price * demand_multiplier
        return round(surge_price, 2)
    
    def get_surge_multiplier(self, num_riders, num_drivers):
        if num_drivers == 0:
            return 3.0
        ratio = num_riders / num_drivers
        if ratio > 5:
            return 2.5
        elif ratio > 3:
            return 1.8
        elif ratio > 2:
            return 1.3
        return 1.0

if __name__ == "__main__":
    print("=" * 50)
    print("   MEMBER 3: PRICING CLIENT")
    print("=" * 50)
    
    engine = PricingEngine()
    
    while True:
        print("\n" + "=" * 50)
        print("OPTIONS:")
        print("1. Calculate price from saved route")
        print("2. Manual price calculation")
        print("3. Quit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            # Load data from Member 1 and Member 2
            route_data = load_data('route.json')
            match_data = load_data('match.json')
            
            if not route_data:
                print("\nERROR: No route data found!")
                print("Please run Member 1 (Routing) first.")
                continue
            
            distance = route_data['distance']
            
            # Get demand info
            if match_data:
                num_drivers = match_data.get('num_available_drivers', 5)
            else:
                num_drivers = 5
            
            num_riders = int(input("Enter current number of riders requesting: "))
            
            surge = engine.get_surge_multiplier(num_riders, num_drivers)
            price = engine.calculate_price(distance, surge)
            
            print(f"\nTRIP PRICING:")
            print(f"   Route: {route_data['start']} -> {route_data['end']}")
            print(f"   Distance: {distance} km")
            print(f"   Demand: {num_riders} riders / {num_drivers} drivers")
            print(f"   Surge Multiplier: {surge}x")
            print(f"   Total Price: ${price}")
            
        elif choice == '2':
            distance = float(input("Enter trip distance (km): "))
            riders = int(input("Enter number of riders: "))
            drivers = int(input("Enter number of drivers: "))
            
            surge = engine.get_surge_multiplier(riders, drivers)
            price = engine.calculate_price(distance, surge)
            
            print(f"\nTrip price: ${price} (Surge: {surge}x)")
            
        elif choice == '3':
            break
    
    print("\nPricing client closed.")
