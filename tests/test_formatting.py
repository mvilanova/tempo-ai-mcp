"""
Unit tests for formatting utilities in tempoai_mcp_server.utils.formatting.

These tests verify that the formatting functions produce expected output strings
for workouts, events, and wellness entries.
"""

from tests.sample_data import (
    SAMPLE_LAP,
    SAMPLE_WORKOUT,
    SAMPLE_WORKOUT_WITH_LAPS,
)

from tempoai_mcp_server.utils.formatting import (
    format_event_details,
    format_event_summary,
    format_wellness_entry,
    format_workout_details,
    format_workout_lap,
    format_workout_summary,
)


# ============================================================================
# Workout Summary Tests
# ============================================================================


def test_format_workout_summary():
    """Test that format_workout_summary returns basic workout info."""
    result = format_workout_summary(SAMPLE_WORKOUT)
    assert "Workout: Morning Ride" in result
    assert "Type: Ride" in result
    assert "Norm Power: 200 W" in result
    assert "Load: 75" in result
    assert "Intensity: 0.85" in result


def test_format_workout_summary_with_laps():
    """Test that format_workout_summary shows lap count when laps are present."""
    result = format_workout_summary(SAMPLE_WORKOUT_WITH_LAPS)
    assert "Laps: 3" in result


def test_format_workout_summary_no_laps():
    """Test that lap count is omitted when no laps are present."""
    result = format_workout_summary(SAMPLE_WORKOUT)
    assert "Laps:" not in result


# ============================================================================
# Workout Details Tests
# ============================================================================


def test_format_workout_details():
    """Test that format_workout_details returns all standard sections."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Workout Details:" in result
    assert "Morning Ride" in result
    assert "Duration:" in result
    assert "Power:" in result
    assert "Heart Rate:" in result
    assert "Training Metrics:" in result
    assert "Energy:" in result
    assert "Source:" in result


def test_format_workout_details_heart_rate_recovery():
    """Test that HR recovery uses best_vagal_rebound."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "HR Recovery: 40 bpm" in result


def test_format_workout_details_with_decoupling():
    """Test that cardiac drift and power fade are displayed."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Decoupling:" in result
    assert "Cardiac Drift: 3.5%" in result
    assert "Power Fade: -1.2%" in result


def test_format_workout_details_no_decoupling():
    """Test that decoupling section is omitted when no decoupling data."""
    workout = {**SAMPLE_WORKOUT, "cardiac_drift": None, "power_fade": None}
    result = format_workout_details(workout)
    assert "Decoupling:" not in result


def test_format_workout_details_with_hr_zones():
    """Test that HR zone distribution is formatted with named labels."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Heart Rate Zones:" in result
    assert "Z1 Recovery: 2m 0s" in result
    assert "Z3 Tempo: 20m 0s" in result


def test_format_workout_details_with_power_zones():
    """Test that power zone distribution is formatted with named labels."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Power Zones:" in result
    assert "Z2 Endurance: 13m 20s" in result


def test_format_workout_details_with_temperature_zones():
    """Test that ambient temperature zone distribution uses named labels."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Temperature Zones:" in result
    assert "Mild: 30m 0s" in result
    assert "Warm: 20m 0s" in result


def test_format_workout_details_no_zones():
    """Test that zone sections are omitted when zone data is missing."""
    workout = {
        **SAMPLE_WORKOUT,
        "time_in_hr_zone": None,
        "time_in_power_zone": None,
        "time_in_temperature_zone": None,
        "time_in_core_temperature_zone": None,
        "time_in_skin_temperature_zone": None,
        "time_in_heat_strain_zone": None,
    }
    result = format_workout_details(workout)
    assert "Heart Rate Zones:" not in result
    assert "Power Zones:" not in result
    assert "Temperature Zones:" not in result
    assert "Core Temperature Zones:" not in result
    assert "Skin Temperature Zones:" not in result
    assert "Heat Strain Zones:" not in result


def test_format_workout_details_with_core_sensor():
    """Test that CORE sensor summary statistics and zone names are displayed."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "CORE Sensor:" in result
    assert "Core Temp: 36.8 / 38.2 / 39.1 °C (min/avg/max)" in result
    assert "Skin Temp: 30.5 / 33.0 / 35.2 °C (min/avg/max)" in result
    assert "Heat Strain: 10.0 / 35.0 / 55.0 Heat Strain Index (min/avg/max)" in result

    # Zone name translations for CORE sensor zones
    assert "Core Temperature Zones:" in result
    assert "Normal: 10m 0s" in result
    assert "Moderate: 30m 0s" in result
    assert "Elevated: 15m 0s" in result

    assert "Skin Temperature Zones:" in result
    assert "Warm: 25m 0s" in result

    assert "Heat Strain Zones:" in result
    assert "No Strain: 40m 0s" in result


def test_format_workout_details_no_core_sensor():
    """Test that CORE sensor section is omitted when no data is present."""
    workout = {
        **SAMPLE_WORKOUT,
        "min_core_temperature": None,
        "avg_core_temperature": None,
        "max_core_temperature": None,
        "min_skin_temperature": None,
        "avg_skin_temperature": None,
        "max_skin_temperature": None,
        "min_heat_strain_index": None,
        "avg_heat_strain_index": None,
        "max_heat_strain_index": None,
    }
    result = format_workout_details(workout)
    assert "CORE Sensor:" not in result


def test_format_workout_details_with_notes():
    """Test that notes are displayed when present."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Notes: Felt strong on the climbs today." in result


def test_format_workout_details_no_notes():
    """Test that notes section is omitted when empty."""
    workout = {**SAMPLE_WORKOUT, "notes": None}
    result = format_workout_details(workout)
    assert "Notes:" not in result


def test_format_workout_details_device_and_timezone():
    """Test that device name and time zone are shown in source section."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Device: Wahoo ELEMNT BOLT" in result
    assert "Time Zone: America/New_York" in result


def test_format_workout_details_with_laps():
    """Test that laps section appears when workout has laps."""
    result = format_workout_details(SAMPLE_WORKOUT_WITH_LAPS)
    assert "Laps (3):" in result
    assert "Lap 1 - Interval 1" in result
    assert "Lap 2 - Recovery" in result
    assert "Lap 3 - Interval 2" in result


def test_format_workout_details_no_laps():
    """Test that laps section is omitted when no laps."""
    result = format_workout_details(SAMPLE_WORKOUT)
    assert "Laps (" not in result


# ============================================================================
# Workout Lap Tests
# ============================================================================


def test_format_workout_lap():
    """Test that format_workout_lap formats a full lap with all metrics."""
    result = format_workout_lap(SAMPLE_LAP)
    assert "Lap 1 - Interval 1" in result
    assert "Elapsed: 5m 0s" in result
    assert "Moving: 4m 55s" in result
    assert "Distance: 3.50 km" in result
    assert "Elevation Gain: 45 m" in result
    assert "Avg Speed: 11.7 m/s" in result
    assert "Max Speed: 14.2 m/s" in result
    assert "Power: Avg 250W / NP 255W / Max 380W" in result
    assert "W/kg: 3.57" in result
    assert "Cadence: 95 rpm" in result
    assert "HR: Avg 160 / Max 172 bpm" in result
    assert "Load: IF 0.92 / VI 1.02 / TSS 12" in result
    assert "Efficiency: EF 1.56 / P:HR 1.56" in result
    assert "VAM: 540 m/h" in result
    assert "Work: 75.0 kJ" in result
    assert "Calories: 85" in result


def test_format_workout_lap_minimal():
    """Test lap formatting with only required fields."""
    lap = {
        "lap_index": 1,
        "start_time": "2024-01-01T08:10:00Z",
        "elapsed_time": 600,
        "source": "strava",
    }
    result = format_workout_lap(lap)
    assert "Lap 1" in result
    assert "Elapsed: 10m 0s" in result
    assert "Power:" not in result
    assert "HR:" not in result


def test_format_workout_lap_no_name():
    """Test lap formatting when name is absent."""
    lap = {
        "lap_index": 5,
        "start_time": "2024-01-01T08:10:00Z",
        "elapsed_time": 120,
        "source": "strava",
    }
    result = format_workout_lap(lap)
    assert "Lap 5" in result
    assert " - " not in result


def test_format_workout_lap_power_only_avg():
    """Test that partial power metrics format correctly."""
    lap = {
        "lap_index": 1,
        "start_time": "2024-01-01T08:10:00Z",
        "elapsed_time": 300,
        "source": "strava",
        "avg_power": 200,
    }
    result = format_workout_lap(lap)
    assert "Power: Avg 200W" in result
    assert "NP" not in result
    assert "Max" not in result


# ============================================================================
# Wellness Tests
# ============================================================================


def test_format_wellness_entry():
    """Test that format_wellness_entry returns a string containing wellness metrics."""
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


# ============================================================================
# Event Tests
# ============================================================================


def test_format_event_summary():
    """Test that format_event_summary returns event name and date."""
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
    """Test that format_event_details returns detailed event info."""
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
