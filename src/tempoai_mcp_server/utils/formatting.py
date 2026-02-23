"""
Formatting utilities for Tempo AI MCP Server

This module contains formatting functions for handling data from the Tempo AI API.
"""

import math
from datetime import datetime
from typing import Any

# Zone name mappings (consistent with iOS and web frontends)
HR_ZONE_NAMES: dict[str, str] = {
    "Z1": "Z1 Recovery",
    "Z2": "Z2 Endurance",
    "Z3": "Z3 Tempo",
    "Z4": "Z4 Threshold",
    "Z5": "Z5 VO2 Max",
}

POWER_ZONE_NAMES: dict[str, str] = {
    "Z1": "Z1 Recovery",
    "Z2": "Z2 Endurance",
    "Z3": "Z3 Tempo",
    "SS": "SS Sweet Spot",
    "Z4": "Z4 Threshold",
    "Z5": "Z5 VO2 Max",
    "Z6": "Z6 Anaerobic",
    "Z7": "Z7 Neuromuscular",
}

TEMPERATURE_ZONE_NAMES: dict[str, str] = {
    "z1_freezing": "Freezing",
    "z2_cold": "Cold",
    "z3_cool": "Cool",
    "z4_mild": "Mild",
    "z5_warm": "Warm",
    "z6_hot": "Hot",
    "z7_extreme": "Extreme",
}

CORE_TEMPERATURE_ZONE_NAMES: dict[str, str] = {
    "z1_low": "Low",
    "z2_normal": "Normal",
    "z3_moderate": "Moderate",
    "z4_elevated": "Elevated",
    "z5_high": "High",
    "z6_very_high": "Very High",
}

SKIN_TEMPERATURE_ZONE_NAMES: dict[str, str] = {
    "z1_cool": "Cool",
    "z2_mild": "Mild",
    "z3_normal": "Normal",
    "z4_warm": "Warm",
    "z5_hot": "Hot",
    "z6_very_hot": "Very Hot",
}

HEAT_STRAIN_ZONE_NAMES: dict[str, str] = {
    "z1_no_strain": "No Strain",
    "z2_moderate": "Moderate",
    "z3_high": "High",
    "z4_extremely_high": "Extremely High",
}

# Power duration curve benchmark durations (in order)
POWER_DURATION_BENCHMARKS = [
    "1s",
    "3s",
    "5s",
    "10s",
    "12s",
    "15s",
    "20s",
    "30s",
    "45s",
    "1min",
    "2min",
    "3min",
    "5min",
    "8min",
    "10min",
    "12min",
    "15min",
    "20min",
    "30min",
    "40min",
    "60min",
    "90min",
    "2h",
    "3h",
    "4h",
    "5h",
]


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


def _format_time_in_zone(
    zone_data: dict[str, Any] | None,
    label: str,
    zone_names: dict[str, str] | None = None,
) -> list[str]:
    """Format a time-in-zone dict into labeled duration lines.

    Args:
        zone_data: Dict mapping zone keys to seconds, e.g. {"Z1": 120.5, "Z2": 300.0}.
        label: Section heading to display, e.g. "Heart Rate Zones".
        zone_names: Optional mapping of zone keys to human-readable names.
            Falls back to the raw key if no mapping is found.

    Returns:
        A list of formatted lines, empty if zone_data is missing or empty.
    """
    if not zone_data or not isinstance(zone_data, dict):
        return []
    lines = [f"{label}:"]
    for zone_key, seconds in zone_data.items():
        display_name = zone_names.get(zone_key, zone_key) if zone_names else zone_key
        lines.append(f"  {display_name}: {_format_duration(seconds)}")
    return lines


def _format_percentage(value: float | None) -> str:
    """Format a percentage value, returning 'N/A' if None."""
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


def _calculate_hrv_score(rmssd: float | int | None) -> int | None:
    """Convert raw RMSSD (ms) to HRV Score using ln(RMSSD) x 20.

    This transformation is used consistently across all Tempo clients (web, iOS,
    MCP) and matches the formula used by ithlete, Morpheus, and Elite HRV.
    It normalizes the exponentially-distributed raw values into a user-friendly
    range (typically 50-100 for healthy adults).

    Args:
        rmssd: Raw RMSSD value in milliseconds.

    Returns:
        HRV Score as a rounded integer, or None if input is invalid.
    """
    if rmssd is None or rmssd <= 0:
        return None
    return round(math.log(rmssd) * 20)


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
        f"  ID: {workout.get('id', 'N/A')}",
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

    laps = workout.get("laps", [])
    if laps and isinstance(laps, list):
        lines.append(f"  Laps: {len(laps)}")

    return "\n".join(lines)


def format_workout_lap(lap: dict[str, Any]) -> str:
    """Format a single workout lap into a readable block.

    Only includes metrics that are present (non-None). Designed for lap/interval
    data returned by WorkoutLapRead from the Tempo AI API.

    Args:
        lap: Dictionary containing lap data.

    Returns:
        A formatted string for the lap.
    """
    lap_index = lap.get("lap_index", "?")
    lap_name = lap.get("name")
    header = f"  Lap {lap_index}"
    if lap_name:
        header += f" - {lap_name}"
    lines = [header]

    # Timing
    elapsed = lap.get("elapsed_time")
    if elapsed is not None:
        lines.append(f"    Elapsed: {_format_duration(elapsed)}")
    moving = lap.get("moving_time")
    if moving is not None:
        lines.append(f"    Moving: {_format_duration(moving)}")

    # Distance & Elevation
    distance = lap.get("distance")
    if distance is not None:
        lines.append(f"    Distance: {_format_distance(distance)}")
    elev_gain = lap.get("total_elevation_gain")
    if elev_gain is not None:
        lines.append(f"    Elevation Gain: {elev_gain:.0f} m")

    # Speed
    avg_speed = lap.get("avg_speed")
    if avg_speed is not None:
        lines.append(f"    Avg Speed: {avg_speed:.1f} m/s")
    max_speed = lap.get("max_speed")
    if max_speed is not None:
        lines.append(f"    Max Speed: {max_speed:.1f} m/s")

    # Power
    power_parts: list[str] = []
    if lap.get("avg_power") is not None:
        power_parts.append(f"Avg {lap['avg_power']}W")
    if lap.get("normalized_power") is not None:
        power_parts.append(f"NP {lap['normalized_power']}W")
    if lap.get("max_power") is not None:
        power_parts.append(f"Max {lap['max_power']}W")
    if power_parts:
        lines.append(f"    Power: {' / '.join(power_parts)}")
    if lap.get("watts_per_kg") is not None:
        lines.append(f"    W/kg: {lap['watts_per_kg']:.2f}")

    # Cadence
    if lap.get("avg_cadence") is not None:
        lines.append(f"    Cadence: {lap['avg_cadence']} rpm")

    # Heart rate
    hr_parts: list[str] = []
    if lap.get("avg_heart_rate") is not None:
        hr_parts.append(f"Avg {lap['avg_heart_rate']}")
    if lap.get("max_heart_rate") is not None:
        hr_parts.append(f"Max {lap['max_heart_rate']}")
    if hr_parts:
        lines.append(f"    HR: {' / '.join(hr_parts)} bpm")

    # Training load
    load_parts: list[str] = []
    if lap.get("intensity_factor") is not None:
        load_parts.append(f"IF {lap['intensity_factor']:.2f}")
    if lap.get("variability_index") is not None:
        load_parts.append(f"VI {lap['variability_index']:.2f}")
    if lap.get("training_stress_score") is not None:
        load_parts.append(f"TSS {lap['training_stress_score']:.0f}")
    if load_parts:
        lines.append(f"    Load: {' / '.join(load_parts)}")

    # Efficiency
    eff_parts: list[str] = []
    if lap.get("efficiency_factor") is not None:
        eff_parts.append(f"EF {lap['efficiency_factor']:.2f}")
    if lap.get("power_hr_ratio") is not None:
        eff_parts.append(f"P:HR {lap['power_hr_ratio']:.2f}")
    if eff_parts:
        lines.append(f"    Efficiency: {' / '.join(eff_parts)}")

    # Climbing
    if lap.get("vam") is not None:
        lines.append(f"    VAM: {lap['vam']:.0f} m/h")

    # Work
    if lap.get("work_joules") is not None:
        lines.append(f"    Work: {lap['work_joules'] / 1000:.1f} kJ")
    if lap.get("calories") is not None:
        lines.append(f"    Calories: {lap['calories']}")

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
    lines.append(f"  Estimated FTP: {_get_value(workout, 'estimated_ftp')} W")
    lines.append(f"  Intensity: {_get_value(workout, 'intensity_factor')}")
    lines.append(f"  Variability Index (VI): {_get_value(workout, 'variability_index')}")
    lines.append(f"  L/R Balance: {_get_value(workout, 'left_right_balance')}")
    lines.append("")

    # Power duration curve
    power_duration_curve = workout.get("power_duration_curve")
    if power_duration_curve and isinstance(power_duration_curve, dict):
        lines.append("Power Duration Curve:")
        for duration in POWER_DURATION_BENCHMARKS:
            if duration in power_duration_curve:
                power = power_duration_curve[duration]
                lines.append(f"  {duration}: {power} W")
        lines.append("")

    # Heart rate metrics
    lines.append("Heart Rate:")
    lines.append(f"  Average HR: {_get_value(workout, 'heart_rate_average')} bpm")
    lines.append(f"  Max HR: {_get_value(workout, 'heart_rate_max')} bpm")
    lines.append(f"  HR Recovery: {_get_value(workout, 'best_vagal_rebound')} bpm")
    lines.append("")

    # Training metrics
    lines.append("Training Metrics:")
    lines.append(f"  Load: {_get_value(workout, 'training_stress_score')}")
    lines.append(f"  Efficiency Factor: {_get_value(workout, 'efficiency_factor')}")
    lines.append(f"  Estimated VO2max: {_get_value(workout, 'estimated_vo2max')}")
    lines.append(f"  Power:HR Ratio: {_get_value(workout, 'power_hr_ratio')}")
    lines.append(f"  Cadence: {_get_value(workout, 'cadence_average')} rpm")
    lines.append("")

    # Decoupling metrics
    if workout.get("cardiac_drift") is not None or workout.get("power_fade") is not None:
        lines.append("Decoupling:")
        if workout.get("cardiac_drift") is not None:
            lines.append(f"  Cardiac Drift: {_format_percentage(workout['cardiac_drift'])}")
        if workout.get("power_fade") is not None:
            lines.append(f"  Power Fade: {_format_percentage(workout['power_fade'])}")
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

    # Time in zone metrics
    hr_zone_lines = _format_time_in_zone(
        workout.get("time_in_hr_zone"), "Heart Rate Zones", HR_ZONE_NAMES
    )
    if hr_zone_lines:
        lines.extend(hr_zone_lines)
        lines.append("")

    power_zone_lines = _format_time_in_zone(
        workout.get("time_in_power_zone"), "Power Zones", POWER_ZONE_NAMES
    )
    if power_zone_lines:
        lines.extend(power_zone_lines)
        lines.append("")

    temp_zone_lines = _format_time_in_zone(
        workout.get("time_in_temperature_zone"), "Temperature Zones", TEMPERATURE_ZONE_NAMES
    )
    if temp_zone_lines:
        lines.extend(temp_zone_lines)
        lines.append("")

    # CORE sensor zones
    core_temp_zone_lines = _format_time_in_zone(
        workout.get("time_in_core_temperature_zone"),
        "Core Temperature Zones",
        CORE_TEMPERATURE_ZONE_NAMES,
    )
    if core_temp_zone_lines:
        lines.extend(core_temp_zone_lines)
        lines.append("")

    skin_temp_zone_lines = _format_time_in_zone(
        workout.get("time_in_skin_temperature_zone"),
        "Skin Temperature Zones",
        SKIN_TEMPERATURE_ZONE_NAMES,
    )
    if skin_temp_zone_lines:
        lines.extend(skin_temp_zone_lines)
        lines.append("")

    heat_strain_zone_lines = _format_time_in_zone(
        workout.get("time_in_heat_strain_zone"), "Heat Strain Zones", HEAT_STRAIN_ZONE_NAMES
    )
    if heat_strain_zone_lines:
        lines.extend(heat_strain_zone_lines)
        lines.append("")

    # CORE sensor summary statistics
    core_fields = [
        ("min_core_temperature", "avg_core_temperature", "max_core_temperature", "Core Temp"),
        ("min_skin_temperature", "avg_skin_temperature", "max_skin_temperature", "Skin Temp"),
        ("min_heat_strain_index", "avg_heat_strain_index", "max_heat_strain_index", "Heat Strain"),
    ]
    core_stats: list[str] = []
    for min_key, avg_key, max_key, label in core_fields:
        min_val = workout.get(min_key)
        avg_val = workout.get(avg_key)
        max_val = workout.get(max_key)
        if any(v is not None for v in (min_val, avg_val, max_val)):
            min_s = f"{min_val:.1f}" if min_val is not None else "N/A"
            avg_s = f"{avg_val:.1f}" if avg_val is not None else "N/A"
            max_s = f"{max_val:.1f}" if max_val is not None else "N/A"
            unit = " Heat Strain Index" if "strain" in min_key else " °C"
            core_stats.append(f"  {label}: {min_s} / {avg_s} / {max_s}{unit} (min/avg/max)")

    if core_stats:
        lines.append("CORE Sensor:")
        lines.extend(core_stats)
        lines.append("")

    # Notes
    if workout.get("notes"):
        lines.append(f"Notes: {workout['notes']}")
        lines.append("")

    # Source info
    lines.append("Source:")
    lines.append(f"  Source: {_get_value(workout, 'source')}")
    if workout.get("device_name"):
        lines.append(f"  Device: {workout['device_name']}")
    if workout.get("time_zone"):
        lines.append(f"  Time Zone: {workout['time_zone']}")
    lines.append(f"  Created: {_format_datetime(workout.get('created_at'))}")
    lines.append(f"  Updated: {_format_datetime(workout.get('updated_at'))}")

    # Laps
    laps = workout.get("laps", [])
    if laps and isinstance(laps, list):
        lines.append("")
        lines.append(f"Laps ({len(laps)}):")
        for lap in laps:
            if isinstance(lap, dict):
                lines.append(format_workout_lap(lap))

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
    hrv_score = _calculate_hrv_score(entry.get("hrv_rmssd"))
    if hrv_score is not None:
        recovery_metrics.append(f"  HRV Score: {hrv_score}")
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
    hrv_baseline_score = _calculate_hrv_score(entry.get("hrv_rmssd_baseline"))
    if hrv_baseline_score is not None:
        baselines.append(f"  HRV Score Baseline: {hrv_baseline_score}")
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
