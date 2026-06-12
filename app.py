from flask import Flask, jsonify, request

from models import (
    Product,
    CartItem,
    Order,
    PRODUCTS,
    CART,
    ORDERS,
    get_product_by_id,
    serialize_products,
    serialize_cart,
    serialize_orders,
)

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "message": "E-commerce backend starter is running",
        "endpoints": [
            "GET /products",
            "POST /products",
            "GET /cart",
            "POST /cart",
            "POST /orders",
            "GET /orders",
        ],
    })


@app.get("/products")
def list_products():
    return jsonify(serialize_products())


@app.post("/products")
def create_product():
    data = request.get_json() or {}

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or price is None or stock is None:
        return jsonify({"error": "name, price, and stock are required"}), 400

    new_product = Product(
        id=len(PRODUCTS) + 1,
        name=name,
        price=float(price),
        stock=int(stock),
    )
    PRODUCTS.append(new_product)
    return jsonify({"message": "Product created", "product": new_product.__dict__}), 201


@app.get("/cart")
def get_cart():
    return jsonify(serialize_cart())


@app.post("/cart")
def add_to_cart():
    data = request.get_json() or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if product_id is None:
        return jsonify({"error": "product_id is required"}), 400

    product = get_product_by_id(int(product_id))
    if not product:
        return jsonify({"error": "product not found"}), 404

    if int(quantity) <= 0:
        return jsonify({"error": "quantity must be greater than zero"}), 400

    if product.stock < int(quantity):
        return jsonify({"error": "not enough stock"}), 400

    CART.append(CartItem(product_id=product.id, quantity=int(quantity)))
    return jsonify({"message": "Added to cart", "cart": serialize_cart()}), 201


@app.post("/orders")
def create_order():
    if not CART:
        return jsonify({"error": "cart is empty"}), 400

    total = 0.0
    order_items = []

    for item in CART:
        product = get_product_by_id(item.product_id)
        if not product:
            return jsonify({"error": f"product {item.product_id} not found"}), 404
        if product.stock < item.quantity:
            return jsonify({"error": f"not enough stock for {product.name}"}), 400

    for item in CART:
        product = get_product_by_id(item.product_id)
        product.stock -= item.quantity
        total += product.price * item.quantity
        order_items.append(CartItem(product_id=item.product_id, quantity=item.quantity))

    new_order = Order(
        id=len(ORDERS) + 1,
        items=order_items,
        total=total,
    )
    ORDERS.append(new_order)
    CART.clear()

    return jsonify({
        "message": "Order created",
        "order": {
            "id": new_order.id,
            "items": [item.__dict__ for item in new_order.items],
            "total": new_order.total,
            "status": new_order.status,
        },
    }), 201


@app.get("/orders")
def list_orders():
    return jsonify(serialize_orders())


if __name__ == "__main__":
    app.run(debug=True)
