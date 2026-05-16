from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.fitness import estimate_steps_calories, estimate_workout_calories
from app.models import ActivityLog, ActivityType, FitnessGoal, GoalMetric, GoalPeriod, User, UserProfile
from app.schemas import ActivityOut, GoalOut, TrendPoint


def _user_weight(db: Session, user_id: int) -> float | None:
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user_id))
    return profile.weight_kg if profile else None


def activity_out(row: ActivityLog) -> ActivityOut:
    return ActivityOut(
        id=str(row.id),
        activity_type=row.activity_type.value,
        category=row.category,
        title=row.title,
        steps=row.steps,
        duration_minutes=row.duration_minutes,
        calories_burned=row.calories_burned,
        notes=row.notes,
        logged_at=row.logged_at.isoformat(),
    )


def period_bounds(period: GoalPeriod, ref: date | None = None) -> tuple[date, date]:
    today = ref or datetime.now(timezone.utc).date()
    if period == GoalPeriod.daily:
        return today, today
    if period == GoalPeriod.weekly:
        start = today - timedelta(days=today.weekday())
        return start, start + timedelta(days=6)
    # monthly
    start = today.replace(day=1)
    if today.month == 12:
        end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    return start, end


def aggregate_metric(
    db: Session,
    user_id: int,
    metric: GoalMetric,
    start: date,
    end: date,
) -> float:
    start_dt = datetime.combine(start, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_dt = datetime.combine(end, datetime.max.time()).replace(tzinfo=timezone.utc)

    q = select(ActivityLog).where(
        ActivityLog.user_id == user_id,
        ActivityLog.logged_at >= start_dt,
        ActivityLog.logged_at <= end_dt,
    )
    rows = db.scalars(q).all()

    if metric == GoalMetric.steps:
        return float(sum(r.steps for r in rows))
    if metric == GoalMetric.calories:
        return float(sum(r.calories_burned for r in rows))
    return float(sum(1 for r in rows if r.activity_type == ActivityType.workout))


def goal_progress(db: Session, goal: FitnessGoal) -> GoalOut:
    start, end = period_bounds(goal.period)
    current = aggregate_metric(db, goal.user_id, goal.metric, start, end)
    target = goal.target_value
    pct = min(100.0, round((current / target) * 100, 1)) if target > 0 else 0.0
    return GoalOut(
        id=str(goal.id),
        metric=goal.metric.value,
        period=goal.period.value,
        target_value=goal.target_value,
        start_date=goal.start_date.isoformat(),
        end_date=goal.end_date.isoformat() if goal.end_date else None,
        is_active=goal.is_active,
        current_value=round(current, 1),
        progress_percent=pct,
    )


def build_activity(
    db: Session,
    user: User,
    *,
    activity_type: ActivityType,
    category: str,
    title: str,
    steps: int,
    duration_minutes: int,
    calories_burned: float | None,
    notes: str,
    logged_at: datetime,
) -> ActivityLog:
    weight = _user_weight(db, user.id)
    calories = calories_burned
    if calories is None:
        if activity_type == ActivityType.steps:
            calories = estimate_steps_calories(steps, weight)
        else:
            calories = estimate_workout_calories(
                category=category, duration_minutes=duration_minutes, weight_kg=weight
            )

    row = ActivityLog(
        user_id=user.id,
        activity_type=activity_type,
        category=category,
        title=title or (f"{steps} steps" if activity_type == ActivityType.steps else category.title()),
        steps=steps,
        duration_minutes=duration_minutes,
        calories_burned=calories,
        notes=notes,
        logged_at=logged_at,
    )
    db.add(row)
    return row


def compute_streak(db: Session, user_id: int) -> int:
    """Consecutive days (including today) with at least one activity log."""
    today = datetime.now(timezone.utc).date()
    streak = 0
    d = today
    while True:
        start_dt = datetime.combine(d, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_dt = datetime.combine(d, datetime.max.time()).replace(tzinfo=timezone.utc)
        count = db.scalar(
            select(func.count())
            .select_from(ActivityLog)
            .where(
                ActivityLog.user_id == user_id,
                ActivityLog.logged_at >= start_dt,
                ActivityLog.logged_at <= end_dt,
            )
        )
        if not count:
            break
        streak += 1
        d -= timedelta(days=1)
    return streak


def build_trends(db: Session, user_id: int, range_days: int) -> list[TrendPoint]:
    today = datetime.now(timezone.utc).date()
    points: list[TrendPoint] = []
    for i in range(range_days - 1, -1, -1):
        d = today - timedelta(days=i)
        start_dt = datetime.combine(d, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_dt = datetime.combine(d, datetime.max.time()).replace(tzinfo=timezone.utc)
        rows = db.scalars(
            select(ActivityLog).where(
                ActivityLog.user_id == user_id,
                ActivityLog.logged_at >= start_dt,
                ActivityLog.logged_at <= end_dt,
            )
        ).all()
        points.append(
            TrendPoint(
                date=d.isoformat(),
                steps=sum(r.steps for r in rows),
                calories=round(sum(r.calories_burned for r in rows), 1),
                workouts=sum(1 for r in rows if r.activity_type == ActivityType.workout),
            )
        )
    return points
