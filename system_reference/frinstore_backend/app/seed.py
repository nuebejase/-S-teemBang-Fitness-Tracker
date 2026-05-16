from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Product, User, UserRole
from app.security import hash_password

ADMIN_EMAIL = "admin@frinstore.com"
ADMIN_PASSWORD = "admin123"

TARGET_PRODUCT_COUNT = 100

MOCK_PRODUCTS: list[dict] = [
    {
        "name": "Strawberry Dream",
        "description": "Creamy strawberry ice cream with real fruit chunks",
        "price": Decimal("150"),
        "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400",
        "category": "Classic",
        "flavor": "Strawberry",
        "stock": 50,
    },
    {
        "name": "Chocolate Paradise",
        "description": "Rich dark chocolate ice cream with chocolate chips",
        "price": Decimal("180"),
        "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400",
        "category": "Classic",
        "flavor": "Chocolate",
        "stock": 45,
    },
    {
        "name": "Vanilla Bliss",
        "description": "Premium Madagascar vanilla bean ice cream",
        "price": Decimal("140"),
        "image": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400",
        "category": "Classic",
        "flavor": "Vanilla",
        "stock": 60,
    },
    {
        "name": "Mango Tango",
        "description": "Tropical mango ice cream with a tangy twist",
        "price": Decimal("160"),
        "image": "https://images.unsplash.com/photo-1560008581-09826d1de69e?w=400",
        "category": "Fruity",
        "flavor": "Mango",
        "stock": 35,
    },
    {
        "name": "Mint Chocolate Chip",
        "description": "Refreshing mint ice cream with chocolate chips",
        "price": Decimal("170"),
        "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=400",
        "category": "Premium",
        "flavor": "Mint",
        "stock": 40,
    },
    {
        "name": "Cookie Monster",
        "description": "Cookies and cream ice cream loaded with Oreo pieces",
        "price": Decimal("190"),
        "image": "https://images.unsplash.com/photo-1567206563064-6f60f40a2b57?w=400",
        "category": "Premium",
        "flavor": "Cookies & Cream",
        "stock": 30,
    },
    {
        "name": "Ube Delight",
        "description": "Filipino favorite purple yam ice cream",
        "price": Decimal("175"),
        "image": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400",
        "category": "Special",
        "flavor": "Ube",
        "stock": 25,
    },
    {
        "name": "Matcha Green Tea",
        "description": "Premium Japanese matcha ice cream",
        "price": Decimal("195"),
        "image": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=400",
        "category": "Premium",
        "flavor": "Matcha",
        "stock": 28,
    },
]

# Rotate for generated rows (Unsplash ice cream / dessert themed)
_IMAGE_URLS = [
    "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400",
    "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400",
    "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400",
    "https://images.unsplash.com/photo-1560008581-09826d1de69e?w=400",
    "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=400",
    "https://images.unsplash.com/photo-1567206563064-6f60f40a2b57?w=400",
    "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400",
    "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=400",
    "https://images.unsplash.com/photo-1557142046-c70493078fd0?w=400",
    "https://images.unsplash.com/photo-1580915411954-282cb1c9b543?w=400",
]

_CATEGORIES = ["Classic", "Premium", "Fruity", "Special"]
_FLAVORS = [
    "Strawberry",
    "Chocolate",
    "Vanilla",
    "Mango",
    "Mint",
    "Ube",
    "Matcha",
    "Coffee",
    "Caramel",
    "Hazelnut",
    "Blueberry",
    "Lemon",
    "Coconut",
    "Pistachio",
    "Black Sesame",
]


def _generated_product_rows(start_index: int, count: int) -> list[dict]:
    rows: list[dict] = []
    for n in range(count):
        i = start_index + n
        cat = _CATEGORIES[i % len(_CATEGORIES)]
        flavor = _FLAVORS[i % len(_FLAVORS)]
        price = Decimal(120 + (i * 7) % 100)
        stock = 15 + (i * 11) % 66
        rows.append(
            {
                "name": f"Scoop Series No. {i:03d}",
                "description": (
                    f"Small-batch {flavor.lower()} ice cream in the {cat} line — "
                    f"creamy, balanced sweetness, ready to ship."
                ),
                "price": price,
                "image": _IMAGE_URLS[i % len(_IMAGE_URLS)],
                "category": cat,
                "flavor": flavor,
                "stock": stock,
            }
        )
    return rows


def seed_if_needed(db: Session) -> None:
    admin = db.scalar(select(User).where(User.email == ADMIN_EMAIL))
    if not admin:
        db.add(
            User(
                email=ADMIN_EMAIL,
                name="Admin User",
                hashed_password=hash_password(ADMIN_PASSWORD),
                role=UserRole.admin,
            )
        )
        db.commit()

    if db.scalar(select(Product.id).limit(1)) is None:
        for row in MOCK_PRODUCTS:
            db.add(Product(**row))
        db.commit()

    count = int(db.scalar(select(func.count()).select_from(Product)) or 0)
    if count < TARGET_PRODUCT_COUNT:
        start = count + 1
        for row in _generated_product_rows(start, TARGET_PRODUCT_COUNT - count):
            db.add(Product(**row))
        db.commit()
