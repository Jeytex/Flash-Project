from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "simple-secret-key"


PRODUCTS = [
    {"id": "him1", "name": "placeholder67", "price": 2499, "image": "images/him1.png", "recommend": "placeholder", "recommend_image": "images/shackles.png"},
    {"id": "him2", "name": "placeholder67", "price": 899, "image": "images/him2.png", "recommend": "placeholder", "recommend_image": "images/chains.png"},
    {"id": "him3", "name": "placeholder67", "price": 3499, "image": "images/him3.png", "recommend": "placeholder", "recommend_image": "images/gloves.png"},
    {"id": "him4", "name": "placeholder67", "price": 2799, "image": "images/him4.png", "recommend": "placeholder", "recommend_image": "images/whip.png"},
    {"id": "him5", "name": "placeholder67", "price": 499, "image": "images/him5.png", "recommend": "placeholder", "recommend_image": "images/brandingiron.png"},
    {"id": "him6", "name": "placeholder67", "price": 1899, "image": "images/him6.png", "recommend": "placeholder", "recommend_image": "images/slavefood.png"},
    {"id": "him7", "name": "placeholder67", "price": 2199, "image": "images/him7.png", "recommend": "placeholder", "recommend_image": "images/sack.png"},
    {"id": "him8", "name": "placeholder67", "price": 699, "image": "images/him8.png", "recommend": "placeholder", "recommend_image": "images/slavebell.png"},
    {"id": "him9", "name": "placeholder67", "price": 1199, "image": "images/him9.png", "recommend": "placeholder", "recommend_image": "images/neckyoke.png"},
]


def find_product(product_id):
    return next((product for product in PRODUCTS if product["id"] == product_id), None)


def cart_items():
    cart = session.get("cart", [])
    items = []

    for product in PRODUCTS:
        quantity = cart.count(product["id"])
        if quantity:
            items.append({
                **product,
                "quantity": quantity,
                "line_total": product["price"] * quantity,
            })

    return items



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
=======
>>>>>>> 37e4956 (commit)
def recommendations():
    cart = session.get("cart", [])
    suggestions = []

    for product_id in cart:
        product = find_product(product_id)
        if product and product["recommend"] not in [item["name"] for item in suggestions]:
            suggestions.append({
                "because": product["name"],
                "name": product["recommend"],
                "image": product["recommend_image"],
            })

    return suggestions


@app.route("/", methods=["GET", "POST"])
def index():
    page = request.args.get("page", "home")

    if request.method == "POST":
        action = request.form.get("action")
        product_id = request.form.get("product")
        cart = session.get("cart", [])

        if action == "add" and find_product(product_id):
            cart.append(product_id)
        elif action == "remove" and product_id in cart:
            cart.remove(product_id)
        elif action == "clear":
            cart = []

        session["cart"] = cart
        page = request.form.get("page", page)

    items = cart_items()

    return render_template(
        "index.html",
        page=page,
        products=PRODUCTS,
        cart_items=items,
        cart_total=sum(item["line_total"] for item in items),
        suggestions=recommendations(),
    )


if __name__ == "__main__":
    app.run(debug=True)
