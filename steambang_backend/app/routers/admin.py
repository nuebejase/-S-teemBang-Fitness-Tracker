from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import AdminUser
from app.models import ActivityLog, ActivityType, FitnessGoal, GoalMetric, User, UserProfile, UserRole
from app.schemas import ActivityOut, AdminStatsOut, AdminUserOut
from app.services import activity_out, aggregate_metric, compute_streak, goal_progress

router = APIRouter(prefix="/admin", tags=["admin"])


def _profile_complete(profile: UserProfile | None) -> bool:
    if not profile:
        return False
    return profile.height_cm is not None and profile.weight_kg is not None and profile.age is not None


def _today_metrics(db: Session, user_id: int) -> tuple[int, float, int]:
    today = datetime.now(timezone.utc).date()
    steps = int(aggregate_metric(db, user_id, GoalMetric.steps, today, today))
    calories = aggregate_metric(db, user_id, GoalMetric.calories, today, today)
    workouts = int(aggregate_metric(db, user_id, GoalMetric.workouts, today, today))
    return steps, round(calories, 1), workouts


@router.get("/stats", response_model=AdminStatsOut)
def admin_stats(_: AdminUser, db: Session = Depends(get_db)):
    total_users = db.scalar(select(func.count()).select_from(User)) or 0
    total_activities = db.scalar(select(func.count()).select_from(ActivityLog)) or 0
    total_goals = db.scalar(select(func.count()).select_from(FitnessGoal)) or 0
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    active_members = db.scalar(
        select(func.count(func.distinct(ActivityLog.user_id))).where(ActivityLog.logged_at >= week_ago)
    ) or 0

    today = datetime.now(timezone.utc).date()
    start_dt = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_dt = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)
    today_rows = db.scalars(
        select(ActivityLog).where(ActivityLog.logged_at >= start_dt, ActivityLog.logged_at <= end_dt)
    ).all()
    today_steps = sum(r.steps for r in today_rows)
    today_calories = round(sum(r.calories_burned for r in today_rows), 1)
    today_workouts = sum(1 for r in today_rows if r.activity_type == ActivityType.workout)

    profiles_complete = 0
    profiles = db.scalars(select(UserProfile)).all()
    for p in profiles:
        if _profile_complete(p):
            profiles_complete += 1

    return AdminStatsOut(
        total_users=total_users,
        total_activities=total_activities,
        total_goals=total_goals,
        active_members=active_members,
        today_platform_steps=today_steps,
        today_platform_calories=today_calories,
        today_platform_workouts=today_workouts,
        profiles_complete=profiles_complete,
    )


@router.get("/users/overview", response_model=list[AdminUserOut])
def users_overview(_: AdminUser, db: Session = Depends(get_db)):
    users = db.scalars(select(User).order_by(User.created_at.desc()).limit(200)).all()
    result: list[AdminUserOut] = []
    for u in users:
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == u.id))
        total_activities = (
            db.scalar(select(func.count()).select_from(ActivityLog).where(ActivityLog.user_id == u.id)) or 0
        )
        total_goals = (
            db.scalar(select(func.count()).select_from(FitnessGoal).where(FitnessGoal.user_id == u.id)) or 0
        )
        last_row = db.scalar(
            select(ActivityLog)
            .where(ActivityLog.user_id == u.id)
            .order_by(ActivityLog.logged_at.desc())
            .limit(1)
        )
        recent = db.scalars(
            select(ActivityLog)
            .where(ActivityLog.user_id == u.id)
            .order_by(ActivityLog.logged_at.desc())
            .limit(8)
        ).all()
        goals = db.scalars(
            select(FitnessGoal).where(FitnessGoal.user_id == u.id, FitnessGoal.is_active.is_(True))
        ).all()
        today_steps, today_calories, today_workouts = _today_metrics(db, u.id)

        result.append(
            AdminUserOut(
                id=str(u.id),
                name=u.name,
                email=u.email,
                role=u.role.value,
                avatar_url=profile.avatar_url if profile else None,
                fitness_level=profile.fitness_level if profile else None,
                profile_complete=_profile_complete(profile),
                daily_step_target=profile.daily_step_target if profile else 8000,
                daily_calorie_target=profile.daily_calorie_target if profile else 500.0,
                daily_workout_target=profile.daily_workout_target if profile else 1,
                today_steps=today_steps,
                today_calories=today_calories,
                today_workouts=today_workouts,
                streak_days=compute_streak(db, u.id) if u.role == UserRole.member else 0,
                total_activities=total_activities,
                total_goals=total_goals,
                last_active=last_row.logged_at.isoformat() if last_row else None,
                active_goals=[goal_progress(db, g) for g in goals],
                recent_activities=[activity_out(r) for r in recent],
            )
        )
    return result


@router.get("/activities", response_model=list[ActivityOut])
def recent_activities(_: AdminUser, db: Session = Depends(get_db), limit: int = 50):
    rows = db.scalars(select(ActivityLog).order_by(ActivityLog.logged_at.desc()).limit(min(limit, 200))).all()
    return [activity_out(r) for r in rows]
