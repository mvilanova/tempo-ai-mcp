"""
Unit tests for formatting utilities in tempoai_mcp_server.utils.formatting.

These tests verify that the formatting functions produce expected output strings
for workouts, events, and wellness entries.
"""

from tempoai_mcp_server.utils.formatting import (
    format_workout_summary,
    format_workout_details,
    format_wellness_entry,
    format_event_summary,
    format_event_details,
)


def test_format_workout_summary():
    """
    Test that format_workout_summary returns a string containing the workout name and type.
    """
    workout = {
        "id": 123,
        "name": "Morning Ride",
        "workout_type": "Ride",
        "start_time": "2024-01-01T08:00:00Z",
        "distance_meters": 25000,
        "duration_total_seconds": 3600,
        "power_normalized": 200,
        "training_stress_score": 75,
    }
    result = format_workout_summary(workout)
    assert "Workout: Morning Ride" in result
    assert "Type: Ride" in result


def test_format_workout_details():
    """
    Test that format_workout_details returns a string containing detailed workout info.
    """
    workout = {
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
        "training_stress_score": 75,
        "heart_rate_average": 145,
    }
    result = format_workout_details(workout)
    assert "Workout Details:" in result
    assert "Morning Ride" in result
    assert "Duration:" in result
    assert "Power:" in result


def test_format_wellness_entry():
    """
    Test that format_wellness_entry returns a string containing wellness metrics.
    """
    entry = {
        "id": 1,
        "date": "2024-01-01",
        "weight_kg": 70.5,
        "resting_hr": 55,
        "hrv_rmssd": 45,
        "sleep_hours": 7.5,
        "readiness_score": 85,
    }
    result = format_wellness_entry(entry)
    assert "Wellness Entry:" in result
    assert "2024-01-01" in result
    assert "70.5 kg" in result
    assert "55 bpm" in result


def test_format_event_summary():
    """
    Test that format_event_summary returns a string containing the event name and date.
    """
    event = {
        "id": 1,
        "name": "Spring Race",
        "event_date": "2024-04-15T08:00:00Z",
        "event_type": "road",
        "status": "planned",
        "location": "Central Park",
    }
    result = format_event_summary(event)
    assert "Event: Spring Race" in result
    assert "ID: 1" in result
    assert "Type: road" in result


def test_format_event_details():
    """
    Test that format_event_details returns a string containing detailed event info.
    """
    event = {
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
    }
    result = format_event_details(event)
    assert "Event Details:" in result
    assert "Spring Race" in result
    assert "Central Park" in result
    assert "100 km" in result
