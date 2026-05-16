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


class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    image: str
    category: str
    flavor: str
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    image: str | None = None
    category: str | None = None
    flavor: str | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductOut(ProductBase):
    id: str

    model_config = {"from_attributes": True}


class OrderLineIn(BaseModel):
    product_id: str
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    items: list[OrderLineIn] = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    customer_email: EmailStr
    customer_phone: str = Field(min_length=1)
    address: str = Field(min_length=1)
    payment_method: str = Field(pattern="^(gcash|card|cod)$")
    delivery_fee: float = Field(default=50, ge=0)


class CartItemOut(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image: str
    category: str
    flavor: str
    stock: int
    quantity: int


class OrderOut(BaseModel):
    id: str
    customer_name: str
    customer_email: str
    customer_phone: str
    address: str
    payment_method: str
    status: str
    date: str
    total: float
    items: list[CartItemOut]


class OrderStatusUpdate(BaseModel):
    status: str = Field(pattern="^(pending|processing|shipped|delivered|cancelled)$")
