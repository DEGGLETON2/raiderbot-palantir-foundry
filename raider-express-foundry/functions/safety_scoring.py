from foundry_functions_api import Function
import numpy as np
from datetime import datetime, timedelta

class SafetyScoringFunction(Function):
    """
    Comprehensive safety scoring for drivers and vehicles
    Focus on 60mph compliance and safe driving practices
    """
    
    def __init__(self):
        super().__init__(
            name="safety_scoring",
            description="Calculate comprehensive safety scores for drivers and vehicles"
        )
    
    def calculate_driver_safety_score(self, driver_id, telemetry_data, incident_history, performance_data):
        """
        Calculate comprehensive driver safety score
        """
        
        # Speed Compliance Score (40% weight)
        speed_score = self._calculate_speed_compliance_score(telemetry_data)
        
        # Driving Behavior Score (30% weight)
        behavior_score = self._calculate_driving_behavior_score(telemetry_data)
        
        # Incident History Score (20% weight)
        incident_score = self._calculate_incident_score(incident_history)
        
        # Performance Correlation Score (10% weight)
        performance_score = self._calculate_performance_correlation_score(performance_data)
        
        # Calculate weighted overall score
        overall_score = (
            speed_score * 0.4 +
            behavior_score * 0.3 +
            incident_score * 0.2 +
            performance_score * 0.1
        )
        
        # Generate recommendations
        recommendations = self._generate_safety_recommendations(
            speed_score, behavior_score, incident_score, performance_score
        )
        
        # Calculate trend analysis
        trend_analysis = self._calculate_safety_trends(driver_id, telemetry_data)
        
        return {
            'driver_id': driver_id,
            'overall_safety_score': round(overall_score, 2),
            'speed_compliance_score': round(speed_score, 2),
            'driving_behavior_score': round(behavior_score, 2),
            'incident_history_score': round(incident_score, 2),
            'performance_correlation_score': round(performance_score, 2),
            'safety_tier': self._get_safety_tier(overall_score),
            'recommendations': recommendations,
            'trend_analysis': trend_analysis,
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_speed_compliance_score(self, telemetry_data):
        """
        Calculate speed compliance score based on 60mph limit
        """
        if not telemetry_data:
            return 50  # Default score for no data
        
        speed_readings = [reading['speed'] for reading in telemetry_data]
        
        # Calculate compliance metrics
        total_readings = len(speed_readings)
        compliant_readings = sum(1 for speed in speed_readings if speed <= 60)
        compliance_rate = compliant_readings / total_readings if total_readings > 0 else 0
        
        # Calculate severity of violations
        violations = [speed - 60 for speed in speed_readings if speed > 60]
        avg_violation_severity = np.mean(violations) if violations else 0
        
        # Base score from compliance rate
        base_score = compliance_rate * 100
        
        # Penalty for violation severity
        severity_penalty = min(avg_violation_severity * 2, 25)
        
        # Penalty for frequency of violations
        violation_frequency = len(violations) / total_readings if total_readings > 0 else 0
        frequency_penalty = violation_frequency * 20
        
        final_score = max(0, base_score - severity_penalty - frequency_penalty)
        
        return final_score
    
    def _calculate_driving_behavior_score(self, telemetry_data):
        """
        Calculate driving behavior score based on harsh events
        """
        if not telemetry_data:
            return 50
        
        # Extract behavior metrics
        harsh_braking_count = sum(1 for reading in telemetry_data if reading.get('harsh_braking', False))
        harsh_acceleration_count = sum(1 for reading in telemetry_data if reading.get('harsh_acceleration', False))
        rapid_lane_changes = sum(1 for reading in telemetry_data if reading.get('rapid_lane_change', False))
        
        total_driving_time = len(telemetry_data)  # Assuming 1 reading per minute
        
        # Calculate rates per hour
        hours_driven = total_driving_time / 60
        harsh_braking_rate = harsh_braking_count / hours_driven if hours_driven > 0 else 0
        harsh_acceleration_rate = harsh_acceleration_count / hours_driven if hours_driven > 0 else 0
        lane_change_rate = rapid_lane_changes / hours_driven if hours_driven > 0 else 0
        
        # Score calculation (100 is perfect)
        base_score = 100
        
        # Penalties for harsh events
        braking_penalty = min(harsh_braking_rate * 5, 30)
        acceleration_penalty = min(harsh_acceleration_rate * 5, 30)
        lane_change_penalty = min(lane_change_rate * 10, 20)
        
        behavior_score = max(0, base_score - braking_penalty - acceleration_penalty - lane_change_penalty)
        
        return behavior_score
    
    def _calculate_incident_score(self, incident_history):
        """
        Calculate score based on incident history
        """
        if not incident_history:
            return 100  # Perfect score for no incidents
        
        # Analyze incidents from last 12 months
        cutoff_date = datetime.now() - timedelta(days=365)
        recent_incidents = [
            incident for incident in incident_history 
            if datetime.fromisoformat(incident['incident_date']) > cutoff_date
        ]
        
        if not recent_incidents:
            return 100
        
        # Weight incidents by severity
        severity_weights = {
            'Low': 1,
            'Medium': 3,
            'High': 7,
            'Critical': 15
        }
        
        total_weight = sum(severity_weights.get(incident['severity'], 1) for incident in recent_incidents)
        
        # Calculate score (more incidents = lower score)
        if total_weight == 0:
            return 100
        elif total_weight <= 3:
            return 90
        elif total_weight <= 7:
            return 75
        elif total_weight <= 15:
            return 60
        else:
            return max(0, 60 - (total_weight - 15) * 2)
    
    def _calculate_performance_correlation_score(self, performance_data):
        """
        Calculate score based on correlation between safety and performance
        """
        if not performance_data:
            return 50
        
        # Factors that correlate with safety
        on_time_rate = performance_data.get('on_time_rate', 0.8)
        customer_satisfaction = performance_data.get('customer_satisfaction', 8.0) / 10
        fuel_efficiency = performance_data.get('fuel_efficiency', 6.0)
        
        # Normalize fuel efficiency (assume 6-8 MPG range for reefer trucks)
        fuel_efficiency_score = min((fuel_efficiency - 4) / 4, 1) if fuel_efficiency > 4 else 0
        
        # Weighted average
        correlation_score = (on_time_rate * 0.4 + customer_satisfaction * 0.3 + fuel_efficiency_score * 0.3) * 100
        
        return correlation_score
    
    def _generate_safety_recommendations(self, speed_score, behavior_score, incident_score, performance_score):
        """
        Generate personalized safety recommendations
        """
        recommendations = []
        
        # Speed-related recommendations
        if speed_score < 80:
            recommendations.append({
                'category': 'Speed Management',
                'priority': 'High',
                'recommendation': 'Focus on maintaining speed at or below 60mph. Consider additional speed awareness training.',
                'action_items': [
                    'Review speed limit policies',
                    'Schedule coaching session on speed management',
                    'Monitor speed compliance daily for next 30 days'
                ]
            })
        
        # Behavior-related recommendations
        if behavior_score < 75:
            recommendations.append({
                'category': 'Driving Behavior',
                'priority': 'Medium',
                'recommendation': 'Work on smooth driving techniques to reduce harsh braking and acceleration events.',
                'action_items': [
                    'Enroll in defensive driving course',
                    'Practice gradual acceleration and deceleration',
                    'Review following distance guidelines'
                ]
            })
        
        # Incident-related recommendations
        if incident_score < 90:
            recommendations.append({
                'category': 'Incident Prevention',
                'priority': 'High',
                'recommendation': 'Focus on incident prevention strategies and situational awareness.',
                'action_items': [
                    'Review recent incident reports',
                    'Complete safety refresher training',
                    'Schedule mentor driver pairing'
                ]
            })
        
        # Performance correlation recommendations
        if performance_score < 70:
            recommendations.append({
                'category': 'Performance Integration',
                'priority': 'Medium',
                'recommendation': 'Align safety practices with performance goals for better overall results.',
                'action_items': [
                    'Review route planning strategies',
                    'Focus on fuel-efficient driving techniques',
                    'Improve customer communication skills'
                ]
            })
        
        return recommendations
    
    def _calculate_safety_trends(self, driver_id, telemetry_data):
        """
        Calculate safety trends over time
        """
        if len(telemetry_data) < 7:  # Need at least a week of data
            return {
                'trend_direction': 'insufficient_data',
                'trend_strength': 0,
                'recent_improvement': False
            }
        
        # Split data into recent and historical
        recent_data = telemetry_data[-7:]  # Last 7 days
        historical_data = telemetry_data[:-7] if len(telemetry_data) > 7 else []
        
        if not historical_data:
            return {
                'trend_direction': 'insufficient_data',
                'trend_strength': 0,
                'recent_improvement': False
            }
        
        # Calculate safety metrics for each period
        recent_speed_violations = sum(1 for reading in recent_data if reading['speed'] > 60)
        historical_speed_violations = sum(1 for reading in historical_data if reading['speed'] > 60)
        
        recent_violation_rate = recent_speed_violations / len(recent_data)
        historical_violation_rate = historical_speed_violations / len(historical_data)
        
        # Determine trend
        if recent_violation_rate < historical_violation_rate:
            trend_direction = 'improving'
            trend_strength = (historical_violation_rate - recent_violation_rate) / historical_violation_rate
        elif recent_violation_rate > historical_violation_rate:
            trend_direction = 'declining'
            trend_strength = (recent_violation_rate - historical_violation_rate) / historical_violation_rate
        else:
            trend_direction = 'stable'
            trend_strength = 0
        
        return {
            'trend_direction': trend_direction,
            'trend_strength': round(trend_strength, 3),
            'recent_improvement': trend_direction == 'improving',
            'recent_violation_rate': round(recent_violation_rate, 3),
            'historical_violation_rate': round(historical_violation_rate, 3)
        }
    
    def _get_safety_tier(self, overall_score):
        """
        Determine safety tier based on overall score
        """
        if overall_score >= 95:
            return 'Exceptional'
        elif overall_score >= 90:
            return 'Excellent'
        elif overall_score >= 80:
            return 'Good'
        elif overall_score >= 70:
            return 'Satisfactory'
        elif overall_score >= 60:
            return 'Needs Improvement'
        else:
            return 'Critical'