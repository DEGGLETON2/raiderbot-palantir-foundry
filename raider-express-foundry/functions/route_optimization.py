from foundry_functions_api import Function
import numpy as np
from scipy.optimize import minimize
from geopy.distance import geodesic
import json
from datetime import datetime

class RouteOptimizationFunction(Function):
    """
    AI-powered route optimization for RaiderBot
    Considers safety-first approach with 60mph speed limits
    """
    
    def __init__(self):
        super().__init__(
            name="route_optimization",
            description="Optimize delivery routes for efficiency and safety"
        )
    
    def execute(self, deliveries, driver_preferences, traffic_data, weather_data):
        """
        Optimize route considering multiple factors
        """
        
        # Extract delivery locations
        locations = []
        for delivery in deliveries:
            locations.append({
                'id': delivery['delivery_id'],
                'lat': delivery['delivery_location']['lat'],
                'lng': delivery['delivery_location']['lng'],
                'time_window_start': delivery['scheduled_delivery_start'],
                'time_window_end': delivery['scheduled_delivery_end'],
                'service_time': delivery.get('estimated_service_time', 30)  # minutes
            })
        
        # Calculate distance matrix
        distance_matrix = self._calculate_distance_matrix(locations)
        
        # Define optimization objective
        def route_cost_function(route_order):
            total_cost = 0
            current_time = 0
            
            for i in range(len(route_order) - 1):
                from_idx = int(route_order[i])
                to_idx = int(route_order[i + 1])
                
                # Distance cost
                distance = distance_matrix[from_idx][to_idx]
                total_cost += distance
                
                # Time cost (at 60mph max speed)
                travel_time = distance / 60  # hours
                current_time += travel_time
                
                # Time window penalty
                delivery = locations[to_idx]
                if current_time < delivery['time_window_start']:
                    # Early arrival - waiting cost
                    total_cost += (delivery['time_window_start'] - current_time) * 10
                elif current_time > delivery['time_window_end']:
                    # Late arrival - penalty cost
                    total_cost += (current_time - delivery['time_window_end']) * 50
                
                # Add service time
                current_time += delivery['service_time'] / 60  # convert to hours
                
                # Traffic penalty
                traffic_multiplier = traffic_data.get(f"{from_idx}_{to_idx}", 1.0)
                total_cost *= traffic_multiplier
                
                # Weather penalty
                weather_multiplier = weather_data.get('safety_multiplier', 1.0)
                total_cost *= weather_multiplier
            
            return total_cost
        
        # Initial route (nearest neighbor heuristic)
        initial_route = self._nearest_neighbor_route(distance_matrix)
        
        # Optimize using simulated annealing
        optimized_route = self._simulated_annealing(
            route_cost_function, 
            initial_route, 
            max_iterations=1000
        )
        
        # Calculate optimization results
        original_cost = route_cost_function(initial_route)
        optimized_cost = route_cost_function(optimized_route)
        
        # Generate turn-by-turn directions
        directions = self._generate_directions(optimized_route, locations)
        
        # Calculate estimated times and distances
        route_summary = self._calculate_route_summary(optimized_route, locations, distance_matrix)
        
        return {
            'optimized_route_order': optimized_route.tolist(),
            'original_cost': original_cost,
            'optimized_cost': optimized_cost,
            'cost_savings': original_cost - optimized_cost,
            'percent_improvement': ((original_cost - optimized_cost) / original_cost) * 100,
            'estimated_total_distance': route_summary['total_distance'],
            'estimated_total_time': route_summary['total_time'],
            'estimated_fuel_consumption': route_summary['fuel_consumption'],
            'safety_score': route_summary['safety_score'],
            'turn_by_turn_directions': directions,
            'optimization_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_distance_matrix(self, locations):
        """Calculate distance matrix between all locations"""
        n = len(locations)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    point1 = (locations[i]['lat'], locations[i]['lng'])
                    point2 = (locations[j]['lat'], locations[j]['lng'])
                    matrix[i][j] = geodesic(point1, point2).miles
        
        return matrix
    
    def _nearest_neighbor_route(self, distance_matrix):
        """Generate initial route using nearest neighbor heuristic"""
        n = len(distance_matrix)
        unvisited = set(range(1, n))  # Start from depot (0)
        current = 0
        route = [0]
        
        while unvisited:
            nearest = min(unvisited, key=lambda x: distance_matrix[current][x])
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        route.append(0)  # Return to depot
        return np.array(route)
    
    def _simulated_annealing(self, cost_function, initial_route, max_iterations=1000):
        """Optimize route using simulated annealing"""
        current_route = initial_route.copy()
        current_cost = cost_function(current_route)
        best_route = current_route.copy()
        best_cost = current_cost
        
        # Simulated annealing parameters
        initial_temp = 100.0
        final_temp = 0.1
        cooling_rate = 0.95
        
        temperature = initial_temp
        
        for iteration in range(max_iterations):
            # Generate neighbor solution (2-opt swap)
            new_route = self._two_opt_swap(current_route)
            new_cost = cost_function(new_route)
            
            # Accept or reject the new solution
            if new_cost < current_cost or np.random.random() < np.exp((current_cost - new_cost) / temperature):
                current_route = new_route
                current_cost = new_cost
                
                # Update best solution
                if new_cost < best_cost:
                    best_route = new_route.copy()
                    best_cost = new_cost
            
            # Cool down
            temperature *= cooling_rate
            if temperature < final_temp:
                break
        
        return best_route
    
    def _two_opt_swap(self, route):
        """Perform 2-opt swap for route improvement"""
        new_route = route.copy()
        n = len(route)
        
        # Select two random positions (excluding depot)
        i = np.random.randint(1, n - 2)
        j = np.random.randint(i + 1, n - 1)
        
        # Reverse the segment between i and j
        new_route[i:j+1] = new_route[i:j+1][::-1]
        
        return new_route
    
    def _calculate_route_summary(self, route, locations, distance_matrix):
        """Calculate comprehensive route summary"""
        total_distance = 0
        total_time = 0
        
        for i in range(len(route) - 1):
            from_idx = route[i]
            to_idx = route[i + 1]
            distance = distance_matrix[from_idx][to_idx]
            total_distance += distance
            total_time += distance / 60  # hours at 60mph max
        
        # Add service times
        for i in range(1, len(route) - 1):  # Exclude depot
            total_time += locations[route[i]]['service_time'] / 60
        
        # Calculate fuel consumption (assume 6 MPG for refrigerated trucks)
        fuel_consumption = total_distance / 6.0
        
        # Safety score (higher is better)
        safety_score = 100 - min(total_time * 2, 50)  # Penalize long routes
        
        return {
            'total_distance': total_distance,
            'total_time': total_time,
            'fuel_consumption': fuel_consumption,
            'safety_score': safety_score
        }
    
    def _generate_directions(self, route, locations):
        """Generate turn-by-turn directions"""
        directions = []
        
        for i in range(len(route) - 1):
            from_idx = route[i]
            to_idx = route[i + 1]
            
            if from_idx == 0:
                directions.append({
                    'step': i + 1,
                    'instruction': f"Start at Raider Express Depot (Fort Worth, TX)",
                    'destination': f"Delivery #{locations[to_idx]['id']}",
                    'estimated_arrival': "TBD"
                })
            elif to_idx == 0:
                directions.append({
                    'step': i + 1,
                    'instruction': f"Return to Raider Express Depot",
                    'destination': "Depot",
                    'estimated_arrival': "TBD"
                })
            else:
                directions.append({
                    'step': i + 1,
                    'instruction': f"Proceed to delivery location",
                    'destination': f"Delivery #{locations[to_idx]['id']}",
                    'estimated_arrival': "TBD"
                })
        
        return directions