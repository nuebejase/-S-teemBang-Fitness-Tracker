from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser
from app.models import FitnessGoal, GoalMetric
from app.schemas import DashboardOut, TrendsOut
from app.services import aggregate_metric, build_trends, compute_streak, goal_progress

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(user: CurrentUser, db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).date()
    week_start = today - timedelta(days=6)

    today_steps = int(aggregate_metric(db, user.id, GoalMetric.steps, today, today))
    today_calories = aggregate_metric(db, user.id, GoalMetric.calories, today, today)
    today_workouts = int(aggregate_metric(db, user.id, GoalMetric.workouts, today, today))

    week_steps = int(aggregate_metric(db, user.id, GoalMetric.steps, week_start, today))
    week_calories = aggregate_metric(db, user.id, GoalMetric.calories, week_start, today)
    week_workouts = int(aggregate_metric(db, user.id, GoalMetric.workouts, week_start, today))

    goals = db.scalars(
        select(FitnessGoal).where(FitnessGoal.user_id == user.id, FitnessGoal.is_active.is_(True))
    ).all()

    return DashboardOut(
        today_steps=today_steps,
        today_calories=round(today_calories, 1),
        today_workouts=today_workouts,
        week_steps=week_steps,
        week_calories=round(week_calories, 1),
        week_workouts=week_workouts,
        active_goals=[goal_progress(db, g) for g in goals],
        streak_days=compute_streak(db, user.id),
    )


@router.get("/trends", response_model=TrendsOut)
def trends(user: CurrentUser, db: Session = Depends(get_db), days: int = 14):
    days = max(7, min(days, 90))
    return TrendsOut(range_days=days, points=build_trends(db, user.id, days))
