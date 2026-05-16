from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser
from app.models import FitnessGoal, GoalMetric, GoalPeriod
from app.schemas import GoalCreate, GoalOut, GoalUpdate
from app.services import goal_progress

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("", response_model=list[GoalOut])
def list_goals(user: CurrentUser, db: Session = Depends(get_db), active_only: bool = False):
    q = select(FitnessGoal).where(FitnessGoal.user_id == user.id).order_by(FitnessGoal.created_at.desc())
    if active_only:
        q = q.where(FitnessGoal.is_active.is_(True))
    rows = db.scalars(q).all()
    return [goal_progress(db, g) for g in rows]


@router.post("", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(body: GoalCreate, user: CurrentUser, db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).date()
    goal = FitnessGoal(
        user_id=user.id,
        metric=GoalMetric(body.metric),
        period=GoalPeriod(body.period),
        target_value=body.target_value,
        start_date=body.start_date or today,
        end_date=body.end_date,
        is_active=True,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal_progress(db, goal)


@router.patch("/{goal_id}", response_model=GoalOut)
def update_goal(goal_id: int, body: GoalUpdate, user: CurrentUser, db: Session = Depends(get_db)):
    goal = db.get(FitnessGoal, goal_id)
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=404, detail="Goal not found")
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(goal, key, value)
    db.commit()
    db.refresh(goal)
    return goal_progress(db, goal)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, user: CurrentUser, db: Session = Depends(get_db)):
    goal = db.get(FitnessGoal, goal_id)
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
