"""
Formatting utilities for Tempo AI MCP Server

This module contains formatting functions for handling data from the Tempo AI API.
"""

from datetime import datetime
from typing import Any


def _format_datetime(dt_value: str | datetime | None) -> str:
    """Format a datetime value into a readable string."""
    if dt_value is None:
        return "N/A"
    if isinstance(dt_value, str):
        try:
            dt = datetime.fromisoformat(dt_value.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return dt_value
    if isinstance(dt_value, datetime):
        return dt_value.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt_value)


def _format_duration(seconds: float | int | None) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds is None:
        return "N/A"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    if minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def _format_distance(meters: float | None) -> str:
    """Format distance in meters to human-readable string."""
    if meters is None:
        return "N/A"
    if meters >= 1000:
        return f"{meters / 1000:.2f} km"
    return f"{meters:.0f} m"


def _get_value(data: dict[str, Any], key: str, default: str = "N/A") -> str:
    """Get a value from dict, returning default if None or missing."""
    value = data.get(key)
    if value is None:
        return default
    return str(value)


# ============================================================================
# Workout Formatters
# ============================================================================


def format_workout_summary(workout: dict[str, Any]) -> str:
    """Format a workout into a summary string for list view.

    Args:
        workout: Dictionary containing workout data from the Tempo AI API.

    Returns:
        A formatted summary string.
    """
    start_time = _format_datetime(workout.get("start_time"))
    duration = _format_duration(workout.get("duration_total_seconds"))
    distance = _format_distance(workout.get("distance_meters"))

    lines = [
        f"Workout: {workout.get('name', 'Unnamed')}",
        # f"  ID: {workout.get('id', 'N/A')}",
        f"  Type: {workout.get('workout_type', 'Unknown')}",
        f"  Date: {start_time}",
        f"  Duration: {duration}",
        f"  Distance: {distance}",
    ]

    # Add key metrics if available
    if workout.get("power_normalized"):
        lines.append(f"  Norm Power: {workout['power_normalized']} W")
    if workout.get("training_stress_score"):
        lines.append(f"  Load: {workout['training_stress_score']}")
    if workout.get("intensity_factor"):
        lines.append(f"  Intensity: {workout['intensity_factor']:.2f}")

    return "\n".join(lines)


def format_workout_details(workout: dict[str, Any]) -> str:
    """Format detailed workout information into a readable string.

    Args:
        workout: Dictionary containing workout data from the Tempo AI API.

    Returns:
        A formatted detailed string.
    """
    lines = ["Workout Details:", ""]

    # Basic info
    lines.append("General Information:")
    lines.append(f"  ID: {workout.get('id', 'N/A')}")
    lines.append(f"  Name: {workout.get('name', 'Unnamed')}")
    lines.append(f"  Type: {workout.get('workout_type', 'Unknown')}")
    lines.append(f"  Status: {workout.get('status', 'N/A')}")
    lines.append(f"  Start Time: {_format_datetime(workout.get('start_time'))}")
    lines.append(f"  End Time: {_format_datetime(workout.get('end_time'))}")
    if workout.get("description"):
        lines.append(f"  Description: {workout['description']}")
    lines.append("")

    # Duration metrics
    lines.append("Duration:")
    lines.append(f"  Total: {_format_duration(workout.get('duration_total_seconds'))}")
    lines.append(f"  Active: {_format_duration(workout.get('duration_active_seconds'))}")
    lines.append(f"  Paused: {_format_duration(workout.get('duration_paused_seconds'))}")
    lines.append("")

    # Distance and elevation
    lines.append("Distance & Elevation:")
    lines.append(f"  Distance: {_format_distance(workout.get('distance_meters'))}")
    lines.append(f"  Elevation Gain: {_get_value(workout, 'elevation_gain')} m")
    lines.append(f"  Elevation Loss: {_get_value(workout, 'elevation_loss')} m")
    lines.append("")

    # Speed metrics
    lines.append("Speed:")
    lines.append(f"  Average Speed: {_get_value(workout, 'speed_average')} m/s")
    lines.append(f"  Max Speed: {_get_value(workout, 'speed_max')} m/s")
    lines.append("")

    # Power metrics
    lines.append("Power:")
    lines.append(f"  Average Power: {_get_value(workout, 'power_average')} W")
    lines.append(f"  Max Power: {_get_value(workout, 'power_max')} W")
    lines.append(f"  Norm Power: {_get_value(workout, 'power_normalized')} W")
    lines.append(f"  5-min Max Power: {_get_value(workout, 'power_5min_max')} W")
    lines.append(f"  Estimated FTP: {_get_value(workout, 'estimated_ftp')} W")
    lines.append(f"  Intensity: {_get_value(workout, 'intensity_factor')}")
    lines.append(f"  L/R Balance: {_get_value(workout, 'left_right_balance')}")
    lines.append("")

    # Heart rate metrics
    lines.append("Heart Rate:")
    lines.append(f"  Average HR: {_get_value(workout, 'heart_rate_average')} bpm")
    lines.append(f"  Max HR: {_get_value(workout, 'heart_rate_max')} bpm")
    lines.append(f"  HR Recovery: {_get_value(workout, 'best_vagal_rebound')}")
    lines.append("")

    # Training metrics
    lines.append("Training Metrics:")
    lines.append(f"  Load: {_get_value(workout, 'training_stress_score')}")
    lines.append(f"  Efficiency Factor: {_get_value(workout, 'efficiency_factor')}")
    lines.append(f"  Estimated VO2max: {_get_value(workout, 'estimated_vo2max')}")
    lines.append(f"  Power:HR Ratio: {_get_value(workout, 'power_hr_ratio')}")
    lines.append(f"  Cadence: {_get_value(workout, 'cadence_average')} rpm")
    lines.append("")

    # Energy metrics
    lines.append("Energy:")
    lines.append(f"  Calories: {_get_value(workout, 'calories')}")
    lines.append(f"  Work (Joules): {_get_value(workout, 'work_joules')}")
    lines.append(f"  Carb Intake: {_get_value(workout, 'carbohydrate_intake')} g")
    lines.append(f"  Carb Used: {_get_value(workout, 'carbohydrate_used')} g")
    lines.append("")

    # Subjective metrics
    if workout.get("feel") or workout.get("perceived_exertion"):
        lines.append("Subjective:")
        if workout.get("feel"):
            lines.append(f"  Feel: {workout['feel']}")
        if workout.get("perceived_exertion"):
            lines.append(f"  RPE: {workout['perceived_exertion']}/10")
        lines.append("")

    # Notes
    # if workout.get("notes"):
    #     lines.append(f"Notes: {workout['notes']}")
    #     lines.append("")

    # AI Coach Insights
    # if workout.get("ai_coach_insights"):
    #     insights = workout["ai_coach_insights"]
    #     lines.append("AI Coach Insights:")
    #     if insights.get("intro"):
    #         lines.append(f"  {insights['intro']}")
    #     if insights.get("insights"):
    #         lines.append(f"  {insights['insights']}")
    #     if insights.get("closing"):
    #         lines.append(f"  {insights['closing']}")
    #     lines.append("")

    # Source info
    lines.append("Source:")
    lines.append(f"  Source: {_get_value(workout, 'source')}")
    # if workout.get("external_strava_activity_id"):
    #     lines.append(f"  Strava ID: {workout['external_strava_activity_id']}")
    lines.append(f"  Created: {_format_datetime(workout.get('created_at'))}")
    lines.append(f"  Updated: {_format_datetime(workout.get('updated_at'))}")

    return "\n".join(lines)


# ============================================================================
# Wellness Formatters
# ============================================================================


def format_wellness_entry(entry: dict[str, Any]) -> str:
    """Format wellness entry data into a readable string.

    Args:
        entry: Dictionary containing wellness data from the Tempo AI API.

    Returns:
        A formatted string representation of the wellness entry.
    """
    lines = ["Wellness Entry:"]

    # Date
    date_value = entry.get("date", entry.get("id", "N/A"))
    lines.append(f"  Date: {date_value}")
    lines.append(f"  ID: {entry.get('id', 'N/A')}")
    lines.append("")

    # Body metrics
    body_metrics = []
    if entry.get("weight_kg") is not None:
        body_metrics.append(f"  Weight: {entry['weight_kg']:.1f} kg")
    if entry.get("body_fat_percentage") is not None:
        body_metrics.append(f"  Body Fat: {entry['body_fat_percentage']:.1f}%")
    if entry.get("hydration_kg") is not None:
        body_metrics.append(f"  Hydration: {entry['hydration_kg']:.1f} kg")

    if body_metrics:
        lines.append("Body Metrics:")
        lines.extend(body_metrics)
        lines.append("")

    # Recovery metrics
    recovery_metrics = []
    if entry.get("sleep_hours") is not None:
        recovery_metrics.append(f"  Sleep: {entry['sleep_hours']:.1f} hours")
    if entry.get("resting_hr") is not None:
        recovery_metrics.append(f"  Resting HR: {entry['resting_hr']} bpm")
    if entry.get("hrv_rmssd") is not None:
        recovery_metrics.append(f"  HRV (RMSSD): {entry['hrv_rmssd']}")
    if entry.get("readiness_score") is not None:
        recovery_metrics.append(f"  Readiness Score: {entry['readiness_score']}")
    if entry.get("vo2max") is not None:
        recovery_metrics.append(f"  VO2max: {entry['vo2max']:.1f} ml/kg/min")

    if recovery_metrics:
        lines.append("Recovery Metrics:")
        lines.extend(recovery_metrics)
        lines.append("")

    # Baselines (7-day rolling averages)
    baselines = []
    if entry.get("hrv_rmssd_baseline") is not None:
        baselines.append(f"  HRV Baseline: {entry['hrv_rmssd_baseline']:.1f}")
    if entry.get("resting_hr_baseline") is not None:
        baselines.append(f"  Resting HR Baseline: {entry['resting_hr_baseline']:.1f} bpm")
    if entry.get("sleep_baseline") is not None:
        baselines.append(f"  Sleep Baseline: {entry['sleep_baseline']:.1f} hours")
    if entry.get("hydration_baseline") is not None:
        baselines.append(f"  Hydration Baseline: {entry['hydration_baseline']:.1f}%")
    if entry.get("vo2max_baseline") is not None:
        baselines.append(f"  VO2max Baseline: {entry['vo2max_baseline']:.1f} ml/kg/min")

    if baselines:
        lines.append("7-Day Baselines:")
        lines.extend(baselines)
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# Event Formatters
# ============================================================================


def format_event_summary(event: dict[str, Any]) -> str:
    """Format a basic event summary into a readable string.

    Args:
        event: Dictionary containing event data from the Tempo AI API.

    Returns:
        A formatted summary string.
    """
    event_date = _format_datetime(event.get("event_date"))

    lines = [
        f"Event: {event.get('name', 'Unnamed')}",
        f"  ID: {event.get('id', 'N/A')}",
        f"  Date: {event_date}",
        f"  Type: {event.get('event_type', 'Unknown')}",
        f"  Status: {event.get('status', 'N/A')}",
    ]

    if event.get("location"):
        lines.append(f"  Location: {event['location']}")
    if event.get("distance_km"):
        lines.append(f"  Distance: {event['distance_km']} km")
    if event.get("description"):
        desc = (
            event["description"][:100] + "..."
            if len(event["description"]) > 100
            else event["description"]
        )
        lines.append(f"  Description: {desc}")

    return "\n".join(lines)


def format_event_details(event: dict[str, Any]) -> str:
    """Format detailed event information into a readable string.

    Args:
        event: Dictionary containing event data from the Tempo AI API.

    Returns:
        A formatted detailed string.
    """
    lines = ["Event Details:", ""]

    # Basic info
    lines.append("General Information:")
    lines.append(f"  Name: {event.get('name', 'Unnamed')}")
    lines.append(f"  ID: {event.get('id', 'N/A')}")
    lines.append(f"  Date: {_format_datetime(event.get('event_date'))}")
    lines.append(f"  Type: {event.get('event_type', 'Unknown')}")
    lines.append(f"  Category: {_get_value(event, 'category')}")
    lines.append(f"  Status: {event.get('status', 'N/A')}")
    if event.get("location"):
        lines.append(f"  Location: {event['location']}")
    if event.get("description"):
        lines.append(f"  Description: {event['description']}")
    lines.append("")

    # Course details
    course_info = []
    if event.get("distance_km"):
        course_info.append(f"  Distance: {event['distance_km']} km")
    if event.get("elevation_gain_m"):
        course_info.append(f"  Elevation Gain: {event['elevation_gain_m']} m")
    if event.get("duration_minutes"):
        course_info.append(f"  Duration: {event['duration_minutes']} min")

    if course_info:
        lines.append("Course Details:")
        lines.extend(course_info)
        lines.append("")

    # Targets
    targets = []
    if event.get("target_tss"):
        targets.append(f"  Target TSS: {event['target_tss']}")
    if event.get("target_intensity_factor"):
        targets.append(f"  Target IF: {event['target_intensity_factor']:.2f}")
    if event.get("target_power_watts"):
        targets.append(f"  Target Power: {event['target_power_watts']} W")
    if event.get("estimated_calories"):
        targets.append(f"  Est. Calories: {event['estimated_calories']}")
    if event.get("estimated_carbs"):
        targets.append(f"  Est. Carbs: {event['estimated_carbs']} g")

    if targets:
        lines.append("Targets & Estimates:")
        lines.extend(targets)
        lines.append("")

    # Settings
    settings = []
    if event.get("auto_calculate_intensity") is not None:
        settings.append(
            f"  Auto Calculate Intensity: {'Yes' if event['auto_calculate_intensity'] else 'No'}"
        )
    if event.get("include_drafting") is not None:
        settings.append(f"  Include Drafting: {'Yes' if event['include_drafting'] else 'No'}")

    if settings:
        lines.append("Settings:")
        lines.extend(settings)
        lines.append("")

    # Links
    links = []
    if event.get("event_website"):
        links.append(f"  Website: {event['event_website']}")
    if event.get("registration_url"):
        links.append(f"  Registration: {event['registration_url']}")
    if event.get("results_url"):
        links.append(f"  Results: {event['results_url']}")

    if links:
        lines.append("Links:")
        lines.extend(links)
        lines.append("")

    # Notes
    if event.get("notes"):
        lines.append(f"Notes: {event['notes']}")
        lines.append("")

    # Metadata
    lines.append("Metadata:")
    if event.get("workout_id"):
        lines.append(f"  Linked Workout ID: {event['workout_id']}")
    lines.append(f"  Created: {_format_datetime(event.get('created_at'))}")
    lines.append(f"  Updated: {_format_datetime(event.get('updated_at'))}")

    return "\n".join(lines)
