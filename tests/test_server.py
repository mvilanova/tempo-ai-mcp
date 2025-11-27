"""
Unit tests for the main MCP server tool functions in tempoai_mcp_server.server.

These tests use monkeypatching to mock API responses and verify the formatting and output of each tool function:
- get_workouts
- get_workout_details
- get_events
- get_event_details
- get_wellness

The tests ensure that the server's public API returns expected strings and handles data correctly.
"""

import asyncio
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
os.environ.setdefault("API_KEY", "test")

from tempoai_mcp_server.server import (
    get_workouts,
    get_workout_details,
    get_events,
    get_event_details,
    get_wellness,
)


def test_get_workouts(monkeypatch):
    """
    Test get_workouts returns a formatted string containing workout details when given a sample workout.
    """
    sample_response = {
        "workouts": [
            {
                "id": 123,
                "name": "Morning Ride",
                "workout_type": "Ride",
                "start_time": "2024-01-01T08:00:00Z",
                "distance_meters": 25000,
                "duration_total_seconds": 3600,
            }
        ],
        "total": 1,
    }

    async def fake_request(*_args, **_kwargs):
        return sample_response

    monkeypatch.setattr("tempoai_mcp_server.api.client.make_tempo_ai_request", fake_request)
    monkeypatch.setattr("tempoai_mcp_server.tools.workouts.make_tempo_ai_request", fake_request)
    result = asyncio.run(get_workouts(limit=1))
    assert "Morning Ride" in result
    assert "Workouts" in result


def test_get_workout_details(monkeypatch):
    """
    Test get_workout_details returns a formatted string with the workout name and details.
    """
    sample = {
        "id": 123,
        "name": "Morning Ride",
        "workout_type": "Ride",
        "start_time": "2024-01-01T08:00:00Z",
        "distance_meters": 25000,
        "duration_total_seconds": 3600,
        "power_normalized": 200,
        "training_stress_score": 75,
    }

    async def fake_request(*_args, **_kwargs):
        return sample

    monkeypatch.setattr("tempoai_mcp_server.api.client.make_tempo_ai_request", fake_request)
    monkeypatch.setattr("tempoai_mcp_server.tools.workouts.make_tempo_ai_request", fake_request)
    result = asyncio.run(get_workout_details(123))
    assert "Workout Details:" in result
    assert "Morning Ride" in result


def test_get_events(monkeypatch):
    """
    Test get_events returns a formatted string containing event details when given a sample event.
    """
    sample_response = {
        "events": [
            {
                "id": 1,
                "name": "Test Event",
                "event_date": "2024-01-01T08:00:00Z",
                "event_type": "road",
                "status": "planned",
                "description": "A test event",
            }
        ],
        "total": 1,
    }

    async def fake_request(*_args, **_kwargs):
        return sample_response

    monkeypatch.setattr("tempoai_mcp_server.api.client.make_tempo_ai_request", fake_request)
    monkeypatch.setattr("tempoai_mcp_server.tools.events.make_tempo_ai_request", fake_request)
    result = asyncio.run(get_events(start_date="2024-01-01", end_date="2024-01-02"))
    assert "Test Event" in result
    assert "Events" in result


def test_get_event_details(monkeypatch):
    """
    Test get_event_details returns a formatted string with event details for a given event ID.
    """
    sample = {
        "id": 1,
        "name": "Test Event",
        "event_date": "2024-01-01T08:00:00Z",
        "event_type": "road",
        "status": "planned",
        "description": "A test event",
        "location": "Test Location",
    }

    async def fake_request(*_args, **_kwargs):
        return sample

    monkeypatch.setattr("tempoai_mcp_server.api.client.make_tempo_ai_request", fake_request)
    monkeypatch.setattr("tempoai_mcp_server.tools.events.make_tempo_ai_request", fake_request)
    result = asyncio.run(get_event_details(1))
    assert "Event Details:" in result
    assert "Test Event" in result


def test_get_wellness(monkeypatch):
    """
    Test get_wellness returns a formatted string containing wellness data.
    """
    sample_response = {
        "wellness": [
            {
                "id": 1,
                "date": "2024-01-01",
                "weight_kg": 70.5,
                "resting_hr": 55,
                "hrv_rmssd": 45,
                "sleep_hours": 7.5,
            }
        ],
        "total": 1,
    }

    async def fake_request(*_args, **_kwargs):
        return sample_response

    monkeypatch.setattr("tempoai_mcp_server.api.client.make_tempo_ai_request", fake_request)
    monkeypatch.setattr("tempoai_mcp_server.tools.wellness.make_tempo_ai_request", fake_request)
    result = asyncio.run(get_wellness())
    assert "Wellness" in result
    assert "2024-01-01" in result
