from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "simple-secret-key"


PRODUCTS = [

    {"id": "laptop", "name": "ASUS Vivobook", "price": 45000, "image": "images/laptop1.jpg"},
    {"id": "phone", "name": "Samsung Galaxy S26", "price": 18000, "image": "images/mobile1.jpg"},
    {"id": "camera", "name": "Sony AES Digital Camera", "price": 32000, "image": "images/camera1.jpg"},
    {"id": "tv", "name" : "TCL 75inch LED", "price": 28000, "image": "images/tv.jpg"},
    {"id": "camera_2", "name": "Kodak Digital Camera", "price": 42000, "image": "images/camera2.jpg."},
    {"id": "ps5", "name": "PS5", "price": 48000, "image": "images/ps5.jpg"},
    {"id": "laptop2", "name": "Macbook Air M4", "price": 82000, "image": "images/laptop2.jpg"},
    {"id": "laptop3", "name": "Lenovo Legion", "price": 111400, "image": "images/laptop3.jpg"},
    {"id": "phone2", "name": "iPhone 17", "price": 89000, "image": "images/mobile2.jpg"},

]

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def find_product(product_id):
    return next((product for product in PRODUCTS if product["id"] == product_id), None)


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart


def get_cart_items():
    items = []
    cart = get_cart()

    for product in PRODUCTS:
        quantity = cart.get(product["id"], 0)
        if quantity:
            items.append({
                **product,
                "quantity": quantity,
                "total": product["price"] * quantity,
            })

    return items


def get_recommendations(product_id, limit=2):
    return [product for product in PRODUCTS if product["id"] != product_id][:limit]


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("products"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username and password:
            session["logged_in"] = True
            session["username"] = username
            session.setdefault("cart", {})
            return redirect(url_for("products"))

        error = "Enter a username and password."

    return render_template("login.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login_old_link():
    return login()


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/products")
@login_required
def products():
    return render_template("products.html", products=PRODUCTS)


@app.route("/add", methods=["POST"])
@login_required
def add_to_cart():
    product_id = request.form.get("product")
    if find_product(product_id):
        cart = get_cart()
        cart[product_id] = cart.get(product_id, 0) + 1
        save_cart(cart)

    return redirect(url_for("products"))


@app.route("/remove", methods=["POST"])
@login_required
def remove_from_cart():
    product_id = request.form.get("product")
    cart = get_cart()

    if cart.get(product_id, 0) > 1:
        cart[product_id] = cart[product_id] - 1
    else:
        cart.pop(product_id, None)

    save_cart(cart)
    return redirect(url_for("cart"))


@app.route("/cart")
@login_required
def cart():
    cart_items = get_cart_items()
    for item in cart_items:
        item["recommendations"] = get_recommendations(item["id"])

    total = sum(item["total"] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/clear", methods=["POST"])
@login_required
def clear_cart():
    save_cart({})
    return redirect(url_for("cart"))

@app.route("/shrek")
def shrek():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True)
