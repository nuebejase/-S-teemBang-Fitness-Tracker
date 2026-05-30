from pathlib import Path
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import AVATARS_DIR, get_db
from app.deps import CurrentUser, DbSession
from app.models import User, UserProfile, UserRole
from app.schemas import ProfileOut, ProfileUpdate, TokenResponse, UserCreate, UserLogin, UserOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_AVATAR_BYTES = 2 * 1024 * 1024


def _user_out(user: User) -> UserOut:
    return UserOut(id=str(user.id), name=user.name, email=user.email, role=user.role.value)


def _profile_complete(profile: UserProfile) -> bool:
    return profile.height_cm is not None and profile.weight_kg is not None and profile.age is not None


def _profile_out(profile: UserProfile) -> ProfileOut:
    return ProfileOut(
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        age=profile.age,
        fitness_level=profile.fitness_level,
        daily_step_target=profile.daily_step_target,
        daily_calorie_target=profile.daily_calorie_target,
        daily_workout_target=profile.daily_workout_target,
        avatar_url=profile.avatar_url,
        is_complete=_profile_complete(profile),
    )


def _ensure_profile(db: Session, user: User) -> UserProfile:
    profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    if profile:
        return profile
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/register", response_model=TokenResponse)
def register(body: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == body.email.lower()))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        email=body.email.lower(),
        name=body.name.strip(),
        hashed_password=hash_password(body.password),
        role=UserRole.member,
    )
    db.add(user)
    db.flush()
    db.add(UserProfile(user_id=user.id))
    db.commit()
    db.refresh(user)
    token = create_access_token(sub=str(user.id), role=user.role.value)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(sub=str(user.id), role=user.role.value)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
def read_me(user: CurrentUser):
    return _user_out(user)


@router.get("/profile", response_model=ProfileOut)
def read_profile(user: CurrentUser, db: DbSession):
    profile = _ensure_profile(db, user)
    return _profile_out(profile)


@router.patch("/profile", response_model=ProfileOut)
def update_profile(body: ProfileUpdate, user: CurrentUser, db: DbSession):
    profile = _ensure_profile(db, user)
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return _profile_out(profile)


@router.post("/profile/avatar", response_model=ProfileOut)
async def upload_avatar(
    user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Image must be JPEG, PNG, WebP, or GIF")
    raw = await file.read()
    if len(raw) > MAX_AVATAR_BYTES:
        raise HTTPException(status_code=400, detail="Image must be under 2 MB")

    ext = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }[file.content_type]
    AVATARS_DIR.mkdir(parents=True, exist_ok=True)

    profile = _ensure_profile(db, user)
    for candidate in AVATARS_DIR.glob(f"{user.id}_*"):
        candidate.unlink(missing_ok=True)
    for candidate in AVATARS_DIR.glob(f"{user.id}.*"):
        candidate.unlink(missing_ok=True)

    filename = f"{user.id}_{uuid.uuid4().hex[:8]}{ext}"
    dest = AVATARS_DIR / filename
    dest.write_bytes(raw)

    profile.avatar_url = f"/uploads/avatars/{filename}"
    db.commit()
    db.refresh(profile)
    return _profile_out(profile)
