from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.fitness import estimate_steps_calories, estimate_workout_calories
from app.models import (
    ActivityLog,
    ActivityType,
    FitnessGoal,
    GoalMetric,
    GoalPeriod,
    Notification,
    NotificationKind,
    User,
    UserProfile,
    UserRole,
)
from app.security import hash_password

ADMIN_EMAIL = "admin@steambang.com"
ADMIN_PASSWORD = "admin123"
DEMO_EMAIL = "demo@steambang.com"
DEMO_PASSWORD = "demo1234"


def seed_if_needed(db: Session) -> None:
    admin = db.scalar(select(User).where(User.email == ADMIN_EMAIL))
    if not admin:
        admin = User(
            email=ADMIN_EMAIL,
            name="System Admin",
            hashed_password=hash_password(ADMIN_PASSWORD),
            role=UserRole.admin,
        )
        db.add(admin)
        db.flush()
        db.add(UserProfile(user_id=admin.id, fitness_level="advanced", daily_step_target=10000))

    demo = db.scalar(select(User).where(User.email == DEMO_EMAIL))
    if not demo:
        demo = User(
            email=DEMO_EMAIL,
            name="Demo Athlete",
            hashed_password=hash_password(DEMO_PASSWORD),
            role=UserRole.member,
        )
        db.add(demo)
        db.flush()
        profile = UserProfile(
            user_id=demo.id,
            height_cm=170,
            weight_kg=68,
            age=22,
            fitness_level="intermediate",
            daily_step_target=10000,
        )
        db.add(profile)
        db.flush()
        _seed_demo_data(db, demo.id, profile.weight_kg)

    db.commit()


def _seed_demo_data(db: Session, user_id: int, weight_kg: float) -> None:
    now = datetime.now(timezone.utc)
    categories = ["running", "strength", "yoga", "cycling", "walking"]
    for i in range(14):
        day = now - timedelta(days=13 - i)
        steps = 6000 + (i * 350) % 5000
        db.add(
            ActivityLog(
                user_id=user_id,
                activity_type=ActivityType.steps,
                category="walking",
                title=f"{steps:,} steps",
                steps=steps,
                duration_minutes=0,
                calories_burned=estimate_steps_calories(steps, weight_kg),
                notes="Seeded demo steps",
                logged_at=day.replace(hour=20, minute=0),
            )
        )
        if i % 2 == 0:
            cat = categories[i % len(categories)]
            mins = 30 + (i * 5) % 40
            db.add(
                ActivityLog(
                    user_id=user_id,
                    activity_type=ActivityType.workout,
                    category=cat,
                    title=f"{cat.title()} session",
                    steps=0,
                    duration_minutes=mins,
                    calories_burned=estimate_workout_calories(category=cat, duration_minutes=mins, weight_kg=weight_kg),
                    notes="Seeded demo workout",
                    logged_at=day.replace(hour=7, minute=30),
                )
            )

    if not db.scalar(select(func.count()).select_from(FitnessGoal).where(FitnessGoal.user_id == user_id)):
        today = now.date()
        db.add_all(
            [
                FitnessGoal(
                    user_id=user_id,
                    metric=GoalMetric.steps,
                    period=GoalPeriod.daily,
                    target_value=10000,
                    start_date=today,
                    is_active=True,
                ),
                FitnessGoal(
                    user_id=user_id,
                    metric=GoalMetric.calories,
                    period=GoalPeriod.weekly,
                    target_value=2500,
                    start_date=today - timedelta(days=today.weekday()),
                    is_active=True,
                ),
                FitnessGoal(
                    user_id=user_id,
                    metric=GoalMetric.workouts,
                    period=GoalPeriod.monthly,
                    target_value=16,
                    start_date=today.replace(day=1),
                    is_active=True,
                ),
            ]
        )

    if not db.scalar(select(func.count()).select_from(Notification).where(Notification.user_id == user_id)):
        db.add_all(
            [
                Notification(
                    user_id=user_id,
                    title="Welcome to (S)TeemBang",
                    body="Log your first workout or sync steps to start your streak.",
                    kind=NotificationKind.system,
                ),
                Notification(
                    user_id=user_id,
                    title="Daily step reminder",
                    body="You're halfway to today's step goal — keep moving!",
                    kind=NotificationKind.reminder,
                ),
            ]
        )
