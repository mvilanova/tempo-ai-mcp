"""
Sample data for testing Tempo AI MCP server functions.

This module contains test data structures used across the test suite.
"""

SAMPLE_WORKOUT = {
    "id": 123,
    "name": "Morning Ride",
    "workout_type": "Ride",
    "status": "completed",
    "start_time": "2024-01-01T08:00:00Z",
    "end_time": "2024-01-01T09:00:00Z",
    "distance_meters": 25000,
    "duration_total_seconds": 3600,
    "duration_active_seconds": 3500,
    "power_normalized": 200,
    "power_average": 180,
    "power_max": 450,
    "training_stress_score": 75,
    "intensity_factor": 0.85,
    "heart_rate_average": 145,
    "heart_rate_max": 175,
    "cadence_average": 90,
    "calories": 850,
}

SAMPLE_EVENT = {
    "id": 1,
    "name": "Spring Race",
    "event_date": "2024-04-15T08:00:00Z",
    "event_type": "road",
    "category": "A",
    "status": "planned",
    "location": "Central Park",
    "description": "Annual spring cycling race",
    "distance_km": 100,
    "elevation_gain_m": 1500,
    "target_tss": 200,
    "target_intensity_factor": 0.90,
}

SAMPLE_WELLNESS = {
    "id": 1,
    "date": "2024-01-01",
    "weight_kg": 70.5,
    "body_fat_percentage": 15.0,
    "resting_hr": 55,
    "hrv_rmssd": 45,
    "sleep_hours": 7.5,
    "readiness_score": 85,
    "vo2max": 55.0,
}
