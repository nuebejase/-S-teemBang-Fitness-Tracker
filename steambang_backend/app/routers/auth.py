from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser
from app.models import User, UserProfile, UserRole
from app.schemas import ProfileOut, ProfileUpdate, TokenResponse, UserCreate, UserLogin, UserOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


def _user_out(user: User) -> UserOut:
    return UserOut(id=str(user.id), name=user.name, email=user.email, role=user.role.value)


def _profile_out(profile: UserProfile) -> ProfileOut:
    return ProfileOut(
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        age=profile.age,
        fitness_level=profile.fitness_level,
        daily_step_target=profile.daily_step_target,
    )


def _ensure_profile(db: Session, user: User) -> UserProfile:
    if user.profile:
        return user.profile
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(user)
    return user.profile  # type: ignore[return-value]


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
def read_profile(user: CurrentUser, db: Session = Depends(get_db)):
    profile = _ensure_profile(db, user)
    return _profile_out(profile)


@router.patch("/profile", response_model=ProfileOut)
def update_profile(body: ProfileUpdate, user: CurrentUser, db: Session = Depends(get_db)):
    profile = _ensure_profile(db, user)
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return _profile_out(profile)
