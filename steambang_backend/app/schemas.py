from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    height_cm: float | None = Field(default=None, gt=0, le=300)
    weight_kg: float | None = Field(default=None, gt=0, le=500)
    age: int | None = Field(default=None, ge=10, le=120)
    fitness_level: str | None = Field(default=None, pattern="^(beginner|intermediate|advanced)$")
    daily_step_target: int | None = Field(default=None, ge=1000, le=100000)


class ProfileOut(BaseModel):
    height_cm: float | None
    weight_kg: float | None
    age: int | None
    fitness_level: str
    daily_step_target: int


class StepsSync(BaseModel):
    steps: int = Field(ge=0)


class ActivityCreate(BaseModel):
    activity_type: str = Field(pattern="^(steps|workout)$")
    category: str = Field(default="general", max_length=80)
    title: str = Field(default="", max_length=255)
    steps: int = Field(default=0, ge=0)
    duration_minutes: int = Field(default=0, ge=0)
    calories_burned: float | None = Field(default=None, ge=0)
    notes: str = Field(default="", max_length=2000)
    logged_at: datetime | None = None


class ActivityUpdate(BaseModel):
    category: str | None = Field(default=None, max_length=80)
    title: str | None = Field(default=None, max_length=255)
    steps: int | None = Field(default=None, ge=0)
    duration_minutes: int | None = Field(default=None, ge=0)
    calories_burned: float | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=2000)
    logged_at: datetime | None = None


class ActivityOut(BaseModel):
    id: str
    activity_type: str
    category: str
    title: str
    steps: int
    duration_minutes: int
    calories_burned: float
    notes: str
    logged_at: str


class GoalCreate(BaseModel):
    metric: str = Field(pattern="^(steps|calories|workouts)$")
    period: str = Field(pattern="^(daily|weekly|monthly)$")
    target_value: float = Field(gt=0)
    start_date: date | None = None
    end_date: date | None = None


class GoalUpdate(BaseModel):
    target_value: float | None = Field(default=None, gt=0)
    is_active: bool | None = None
    end_date: date | None = None


class GoalOut(BaseModel):
    id: str
    metric: str
    period: str
    target_value: float
    start_date: str
    end_date: str | None
    is_active: bool
    current_value: float
    progress_percent: float


class NotificationOut(BaseModel):
    id: str
    title: str
    body: str
    kind: str
    is_read: bool
    created_at: str


class NotificationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(default="", max_length=2000)
    kind: str = Field(default="reminder", pattern="^(reminder|achievement|system)$")


class DashboardOut(BaseModel):
    today_steps: int
    today_calories: float
    today_workouts: int
    week_steps: int
    week_calories: float
    week_workouts: int
    active_goals: list[GoalOut]
    streak_days: int


class TrendPoint(BaseModel):
    date: str
    steps: int
    calories: float
    workouts: int


class TrendsOut(BaseModel):
    range_days: int
    points: list[TrendPoint]


class AdminStatsOut(BaseModel):
    total_users: int
    total_activities: int
    total_goals: int
    active_members: int
