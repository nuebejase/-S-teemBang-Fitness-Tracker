from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import AdminUser
from app.models import Product
from app.schemas import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


def _product_out(p: Product) -> ProductOut:
    return ProductOut(
        id=str(p.id),
        name=p.name,
        description=p.description,
        price=float(p.price),
        image=p.image,
        category=p.category,
        flavor=p.flavor,
        stock=p.stock,
    )


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    rows = db.query(Product).order_by(Product.id).all()
    return [_product_out(p) for p in rows]


@router.post("", response_model=ProductOut)
def create_product(body: ProductCreate, _: AdminUser, db: Session = Depends(get_db)):
    p = Product(
        name=body.name.strip(),
        description=body.description.strip(),
        price=Decimal(str(body.price)),
        image=body.image.strip(),
        category=body.category.strip(),
        flavor=body.flavor.strip(),
        stock=body.stock,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return _product_out(p)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, body: ProductUpdate, _: AdminUser, db: Session = Depends(get_db)):
    try:
        pid = int(product_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    data = body.model_dump(exclude_unset=True)
    for key, val in data.items():
        if key == "price" and val is not None:
            setattr(p, key, Decimal(str(val)))
        elif val is not None:
            setattr(p, key, val)
    db.commit()
    db.refresh(p)
    return _product_out(p)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, _: AdminUser, db: Session = Depends(get_db)):
    try:
        pid = int(product_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(p)
    db.commit()
    return None
