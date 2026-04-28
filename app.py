from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "simple-secret-key"


PRODUCTS = [
    {
        "id": "him1",
        "name": "Himanshu",
        "price": 2499,
        "image": "images/him1.png",
        "recommend": "Shackles",
        "recommend_image": "images/shackles.png",
    },
    {
        "id": "him2",
        "name": "Himanshu",
        "price": 899,
        "image": "images/him2.png",
        "recommend": "Chains",
        "recommend_image": "images/chains.png",
    },
    {
        "id": "him3",
        "name": "Himanshu",
        "price": 3499,
        "image": "images/him3.png",
        "recommend": "Cotton Picking gloves",
        "recommend_image": "images/gloves.png",
    },
    {
        "id": "him4",
        "name": "Himanshu",
        "price": 2799,
        "image": "images/him4.png",
        "recommend": "Whip",
        "recommend_image": "images/whip.png",
    },
    {
        "id": "him5",
        "name": "Himanshu",
        "price": 499,
        "image": "images/him5.png",
        "recommend": "Branding iron",
        "recommend_image": "images/brandingiron.png",
    },
    {
        "id": "him6",
        "name": "Himanshu",
        "price": 1899,
        "image": "images/him6.png",
        "recommend": "Slave food",
        "recommend_image": "images/slavefood.png",
    },
    {
        "id": "him7",
        "name": "Himanshu",
        "price": 2199,
        "image": "images/him7.png",
        "recommend": "Cotton sack",
        "recommend_image": "images/sack.png",
    },
    {
        "id": "him8",
        "name": "Himanshu",
        "price": 699,
        "image": "images/him8.png",
        "recommend": "Slave bell",
        "recommend_image": "images/slavebell.png",
    },
    {
        "id": "him9",
        "name": "Himanshu",
        "price": 1199,
        "image": "images/him9.png",
        "recommend": "Iron collar",
        "recommend_image": "images/neckyoke.png",
    },
]


def find_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart


def get_cart_count(product_id):
    count = 0
    for item_id in get_cart():
        if item_id == product_id:
            count = count + 1
    return count


def get_cart_items():
    cart_items = []

    for product in PRODUCTS:
        count = get_cart_count(product["id"])
        if count > 0:
            cart_items.append({
                "id": product["id"],
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
    return render_template("login.html")


@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS)


@app.route("/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product")
    product = find_product(product_id)

    if product:
        cart = get_cart()
        cart.append(product["id"])
        save_cart(cart)

    return redirect(url_for("products"))


@app.route("/remove", methods=["POST"])
def remove_from_cart():
    product_id = request.form.get("product")
    cart = get_cart()

    if product_id in cart:
        cart.remove(product_id)
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

    for product_id in get_cart():
        product = find_product(product_id)
        if product:
            suggestion = {
                "because": product["name"],
                "name": product["recommend"],
                "image": url_for("static", filename=product["recommend_image"]),
            }

            if suggestion not in suggestions:
                suggestions.append(suggestion)

    return render_template("recommend.html", suggestions=suggestions)


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
