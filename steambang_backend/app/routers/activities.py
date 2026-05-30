from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser
from app.models import ActivityLog, ActivityType
from app.schemas import ActivityCreate, ActivityOut, ActivityUpdate, StepsSync
from app.services import activity_out, build_activity, check_and_notify_goal_achievements

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("", response_model=list[ActivityOut])
def list_activities(user: CurrentUser, db: Session = Depends(get_db), limit: int = 100):
    rows = db.scalars(
        select(ActivityLog)
        .where(ActivityLog.user_id == user.id)
        .order_by(ActivityLog.logged_at.desc())
        .limit(min(limit, 500))
    ).all()
    return [activity_out(r) for r in rows]


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(body: ActivityCreate, user: CurrentUser, db: Session = Depends(get_db)):
    atype = ActivityType(body.activity_type)
    if atype == ActivityType.steps and body.steps <= 0:
        raise HTTPException(status_code=400, detail="Steps must be greater than zero for step logs")
    if atype == ActivityType.workout and body.duration_minutes <= 0:
        raise HTTPException(status_code=400, detail="Duration must be greater than zero for workouts")

    logged_at = body.logged_at or datetime.now(timezone.utc)
    row = build_activity(
        db,
        user,
        activity_type=atype,
        category=body.category,
        title=body.title,
        steps=body.steps,
        duration_minutes=body.duration_minutes,
        calories_burned=body.calories_burned,
        notes=body.notes,
        logged_at=logged_at,
    )
    db.commit()
    db.refresh(row)
    check_and_notify_goal_achievements(db, user.id)
    return activity_out(row)


@router.post("/steps/sync", response_model=ActivityOut)
def sync_steps(body: StepsSync, user: CurrentUser, db: Session = Depends(get_db)):
    """Upsert today's step count (device pedometer sync)."""
    steps = body.steps
    today = datetime.now(timezone.utc).date()
    start = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)

    existing = db.scalar(
        select(ActivityLog).where(
            ActivityLog.user_id == user.id,
            ActivityLog.activity_type == ActivityType.steps,
            ActivityLog.logged_at >= start,
            ActivityLog.logged_at <= end,
        )
    )
    if existing:
        from app.fitness import estimate_steps_calories
        from app.services import _user_weight

        existing.steps = steps
        existing.calories_burned = estimate_steps_calories(steps, _user_weight(db, user.id))
        existing.title = f"{steps:,} steps today"
        db.commit()
        db.refresh(existing)
        check_and_notify_goal_achievements(db, user.id)
        return activity_out(existing)

    logged_at = datetime.now(timezone.utc)
    row = build_activity(
        db,
        user,
        activity_type=ActivityType.steps,
        category="walking",
        title=f"{steps:,} steps today",
        steps=steps,
        duration_minutes=0,
        calories_burned=None,
        notes="Synced from device pedometer",
        logged_at=logged_at,
    )
    db.commit()
    db.refresh(row)
    check_and_notify_goal_achievements(db, user.id)
    return activity_out(row)


@router.patch("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: int,
    body: ActivityUpdate,
    user: CurrentUser,
    db: Session = Depends(get_db),
):
    row = db.get(ActivityLog, activity_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return activity_out(row)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, user: CurrentUser, db: Session = Depends(get_db)):
    row = db.get(ActivityLog, activity_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(row)
    db.commit()
