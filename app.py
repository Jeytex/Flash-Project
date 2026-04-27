from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "simple-secret-key"


PRODUCTS = [
    {
        "name": "Rose Gold Watch",
        "price": 2499,
        "image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=600&q=80",
        "recommend": "Pearl Bracelet",
        "recommend_image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Canvas Tote Bag",
        "price": 899,
        "image": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=600&q=80",
        "recommend": "Silk Scarf",
        "recommend_image": "https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Wireless Earbuds",
        "price": 3499,
        "image": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?auto=format&fit=crop&w=600&q=80",
        "recommend": "Charging Case",
        "recommend_image": "https://images.unsplash.com/photo-1603539444875-76e7684265f6?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Minimal Sneakers",
        "price": 2799,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80",
        "recommend": "Cotton Socks",
        "recommend_image": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Ceramic Mug",
        "price": 499,
        "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=600&q=80",
        "recommend": "Coffee Beans",
        "recommend_image": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Desk Lamp",
        "price": 1899,
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        "recommend": "Notebook Set",
        "recommend_image": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Cotton Hoodie",
        "price": 2199,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80",
        "recommend": "Denim Cap",
        "recommend_image": "https://images.unsplash.com/photo-1521369909029-2afed882baee?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Scented Candle",
        "price": 699,
        "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=600&q=80",
        "recommend": "Room Diffuser",
        "recommend_image": "https://images.unsplash.com/photo-1616077167599-cad3639f9cbd?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Leather Journal",
        "price": 1199,
        "image": "https://images.unsplash.com/photo-1531346680769-a1d79b57de5c?auto=format&fit=crop&w=600&q=80",
        "recommend": "Fine Pen",
        "recommend_image": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=600&q=80",
    },
]


def find_product(product_name):
    for product in PRODUCTS:
        if product["name"] == product_name:
            return product
    return None


def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart


def get_cart_count(product_name):
    count = 0
    for item_name in get_cart():
        if item_name == product_name:
            count = count + 1
    return count


def get_cart_items():
    cart_items = []

    for product in PRODUCTS:
        count = get_cart_count(product["name"])
        if count > 0:
            cart_items.append({
                "name": product["name"],
                "price": product["price"],
                "image": product["image"],
                "count": count,
                "total": product["price"] * count,
            })

    return cart_items


def get_cart_total():
    total = 0

    for item in get_cart_items():
        total = total + item["total"]

    return total


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS)


@app.route("/add", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product")
    product = find_product(product_name)

    if product:
        cart = get_cart()
        cart.append(product["name"])
        save_cart(cart)

    return redirect(url_for("products"))


@app.route("/remove", methods=["POST"])
def remove_from_cart():
    product_name = request.form.get("product")
    cart = get_cart()

    if product_name in cart:
        cart.remove(product_name)
        save_cart(cart)

    return redirect(url_for("products"))


@app.route("/cart")
def cart():
    return render_template(
        "cart.html",
        cart_items=get_cart_items(),
        total=get_cart_total()
    )


@app.route("/clear", methods=["POST"])
def clear_cart():
    save_cart([])
    return redirect(url_for("cart"))


@app.route("/recommendations")
def recommendations():
    suggestions = []

    for product_name in get_cart():
        product = find_product(product_name)
        if product:
            suggestion = {
                "because": product["name"],
                "name": product["recommend"],
                "image": product["recommend_image"],
            }

            if suggestion not in suggestions:
                suggestions.append(suggestion)

    return render_template("recommendations.html", suggestions=suggestions)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/store")
def old_store_link():
    return redirect(url_for("products"))


@app.route("/home")
def old_home_link():
    return redirect(url_for("home"))


@app.route("/recommend")
def old_recommend_link():
    return redirect(url_for("recommendations"))


if __name__ == "__main__":
    app.run(debug=True)
