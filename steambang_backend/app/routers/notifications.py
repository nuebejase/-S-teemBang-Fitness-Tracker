from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser
from app.models import Notification, NotificationKind
from app.schemas import NotificationCreate, NotificationOut

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _notif_out(row: Notification) -> NotificationOut:
    return NotificationOut(
        id=str(row.id),
        title=row.title,
        body=row.body,
        kind=row.kind.value,
        is_read=row.is_read,
        created_at=row.created_at.isoformat(),
    )


@router.get("", response_model=list[NotificationOut])
def list_notifications(user: CurrentUser, db: Session = Depends(get_db), unread_only: bool = False):
    q = select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc())
    if unread_only:
        q = q.where(Notification.is_read.is_(False))
    rows = db.scalars(q.limit(100)).all()
    return [_notif_out(r) for r in rows]


@router.post("", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_reminder(body: NotificationCreate, user: CurrentUser, db: Session = Depends(get_db)):
    row = Notification(
        user_id=user.id,
        title=body.title,
        body=body.body,
        kind=NotificationKind(body.kind),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _notif_out(row)


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_read(notification_id: int, user: CurrentUser, db: Session = Depends(get_db)):
    row = db.get(Notification, notification_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Notification not found")
    row.is_read = True
    db.commit()
    db.refresh(row)
    return _notif_out(row)


@router.post("/mark-all-read", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_read(user: CurrentUser, db: Session = Depends(get_db)):
    rows = db.scalars(select(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))).all()
    for row in rows:
        row.is_read = True
    db.commit()
