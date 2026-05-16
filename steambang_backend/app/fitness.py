"""Calorie estimation using MET values (approximate, coursework-friendly)."""

MET_BY_CATEGORY: dict[str, float] = {
    "walking": 3.5,
    "running": 9.8,
    "cycling": 7.5,
    "strength": 6.0,
    "yoga": 3.0,
    "hiit": 8.0,
    "swimming": 7.0,
    "other": 5.0,
    "general": 4.0,
}


def estimate_workout_calories(
    *,
    category: str,
    duration_minutes: int,
    weight_kg: float | None = None,
) -> float:
    """Calories ≈ MET × weight(kg) × hours."""
    met = MET_BY_CATEGORY.get(category.lower(), MET_BY_CATEGORY["other"])
    weight = weight_kg if weight_kg and weight_kg > 0 else 70.0
    hours = max(duration_minutes, 1) / 60.0
    return round(met * weight * hours, 1)


def estimate_steps_calories(steps: int, weight_kg: float | None = None) -> float:
    """Roughly 0.04 kcal per step per kg baseline (scaled)."""
    weight = weight_kg if weight_kg and weight_kg > 0 else 70.0
    return round(steps * 0.0005 * weight, 1)
