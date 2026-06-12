from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int


@dataclass
class CartItem:
    product_id: int
    quantity: int


@dataclass
class Order:
    id: int
    items: List[CartItem]
    total: float
    status: str = "created"


PRODUCTS = [
    Product(id=1, name="Laptop", price=75000.0, stock=5),
    Product(id=2, name="Phone", price=25000.0, stock=10),
    Product(id=3, name="Headphones", price=3000.0, stock=20),
]

CART = []
ORDERS = []


def serialize_products():
    return [asdict(product) for product in PRODUCTS]


def get_product_by_id(product_id: int):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    return None


def serialize_cart():
    return [asdict(item) for item in CART]


def serialize_orders():
    return [
        {
            "id": order.id,
            "items": [asdict(item) for item in order.items],
            "total": order.total,
            "status": order.status,
        }
        for order in ORDERS
    ]
