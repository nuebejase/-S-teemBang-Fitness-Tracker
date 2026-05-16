from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import AdminUser
from app.models import ActivityLog, FitnessGoal, User, UserRole
from app.schemas import ActivityOut, AdminStatsOut, UserOut
from app.services import activity_out

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsOut)
def admin_stats(_: AdminUser, db: Session = Depends(get_db)):
    total_users = db.scalar(select(func.count()).select_from(User)) or 0
    total_activities = db.scalar(select(func.count()).select_from(ActivityLog)) or 0
    total_goals = db.scalar(select(func.count()).select_from(FitnessGoal)) or 0
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    active_members = db.scalar(
        select(func.count(func.distinct(ActivityLog.user_id))).where(ActivityLog.logged_at >= week_ago)
    ) or 0
    return AdminStatsOut(
        total_users=total_users,
        total_activities=total_activities,
        total_goals=total_goals,
        active_members=active_members,
    )


@router.get("/users", response_model=list[UserOut])
def list_users(_: AdminUser, db: Session = Depends(get_db)):
    rows = db.scalars(select(User).order_by(User.created_at.desc()).limit(200)).all()
    return [UserOut(id=str(u.id), name=u.name, email=u.email, role=u.role.value) for u in rows]


@router.get("/activities", response_model=list[ActivityOut])
def recent_activities(_: AdminUser, db: Session = Depends(get_db), limit: int = 50):
    rows = db.scalars(select(ActivityLog).order_by(ActivityLog.logged_at.desc()).limit(min(limit, 200))).all()
    return [activity_out(r) for r in rows]
