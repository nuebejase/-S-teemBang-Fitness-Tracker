import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import AdminUser, CurrentUser
from app.models import Order, OrderItem, OrderStatus, Product, UserRole
from app.schemas import CartItemOut, OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


def _item_out(it: OrderItem) -> CartItemOut:
    pid = str(it.product_id) if it.product_id is not None else f"line-{it.id}"
    return CartItemOut(
        id=pid,
        name=it.name,
        description=it.description,
        price=float(it.price),
        image=it.image,
        category=it.category,
        flavor=it.flavor,
        stock=it.stock_at_sale,
        quantity=it.quantity,
    )


def _order_out(order: Order) -> OrderOut:
    items = [_item_out(it) for it in sorted(order.items, key=lambda x: x.id)]
    return OrderOut(
        id=order.id,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        address=order.address,
        payment_method=order.payment_method,
        status=order.status.value,
        date=order.created_at.isoformat(),
        total=float(order.total),
        items=items,
    )


@router.post("", response_model=OrderOut)
def create_order(body: OrderCreate, user: CurrentUser, db: Session = Depends(get_db)):
    if user.role != UserRole.customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customer accounts can place orders")

    lines: list[tuple[Product, int]] = []
    subtotal = Decimal("0")

    for line in body.items:
        try:
            pid = int(line.product_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid product id: {line.product_id}")
        product = db.get(Product, pid)
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product not found: {line.product_id}")
        if product.stock < line.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}",
            )
        unit = Decimal(str(product.price))
        subtotal += unit * line.quantity
        lines.append((product, line.quantity))

    delivery = Decimal(str(body.delivery_fee))
    total = subtotal + delivery
    order_id = f"FS-{uuid.uuid4().hex[:12].upper()}"

    order = Order(
        id=order_id,
        user_id=user.id,
        customer_name=body.customer_name.strip(),
        customer_email=str(body.customer_email).lower(),
        customer_phone=body.customer_phone.strip(),
        address=body.address.strip(),
        payment_method=body.payment_method,
        status=OrderStatus.pending,
        subtotal=subtotal,
        delivery_fee=delivery,
        total=total,
    )
    db.add(order)
    db.flush()

    for product, qty in lines:
        snapshot_stock = int(product.stock)
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                image=product.image,
                category=product.category,
                flavor=product.flavor,
                stock_at_sale=snapshot_stock,
                quantity=qty,
            )
        )
        product.stock = product.stock - qty

    db.commit()
    db.refresh(order)
    order = (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.id == order.id)
        .one()
    )
    return _order_out(order)


@router.get("/me", response_model=list[OrderOut])
def my_orders(user: CurrentUser, db: Session = Depends(get_db)):
    if user.role != UserRole.customer:
        return []
    rows = (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_order_out(o) for o in rows]


@router.get("", response_model=list[OrderOut])
def list_orders_admin(_: AdminUser, db: Session = Depends(get_db)):
    rows = (
        db.query(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_order_out(o) for o in rows]


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_status(order_id: str, body: OrderStatusUpdate, _: AdminUser, db: Session = Depends(get_db)):
    order = db.query(Order).options(selectinload(Order.items)).filter(Order.id == order_id).one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    try:
        order.status = OrderStatus(body.status)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    db.commit()
    db.refresh(order)
    order = (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.id == order_id)
        .one()
    )
    return _order_out(order)
