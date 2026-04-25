from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)

# Flask uses this key to keep session data secure.
# For a real project, use a long random value instead.
app.secret_key = "replace_this_with_a_random_secret"


# These are the products shown on the home page.
products = [
    {"name": "Mobile", "price": 10000},
    {"name": "Laptop", "price": 50000},
    {"name": "Headphones", "price": 2000},
]


def get_cart():
    """Get the cart from the browser session."""
    if "cart" not in session:
        session["cart"] = []

    return session["cart"]


def save_cart(cart):
    """Save the latest cart back into the browser session."""
    session["cart"] = cart


def summarize_cart(cart):
    """Group repeated cart items and count their quantity."""
    cart_summary = []

    for item in cart:
        item_already_added = False

        for summary_item in cart_summary:
            if summary_item["name"] == item["name"]:
                summary_item["quantity"] = summary_item["quantity"] + 1
                item_already_added = True

        if not item_already_added:
            cart_summary.append(
                {
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": 1,
                }
            )

    return cart_summary


def calculate_total(cart):
    """Add the price of every item in the cart."""
    total = 0

    for item in cart:
        total = total + item["price"]

    return total


def find_product(product_name):
    """Find one product by its name."""
    for product in products:
        if product["name"] == product_name:
            return product

    return None


@app.route("/")
def home():
    cart = get_cart()
    cart_summary = summarize_cart(cart)
    total = calculate_total(cart)

    return render_template(
        "index.html",
        products=products,
        cart=cart_summary,
        total=total,
    )


@app.route("/add", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product")
    product = find_product(product_name)

    if product is not None:
        cart = get_cart()
        cart.append(product)
        save_cart(cart)

    return redirect(url_for("home"))


@app.route("/clear", methods=["POST"])
def clear_cart():
    save_cart([])
    return redirect(url_for("home"))


@app.route("/recommend")
def recommend():
    cart = get_cart()
    suggestions = []

    for item in cart:
        if item["name"] == "Mobile":
            suggestions.append("Charger")
        elif item["name"] == "Laptop":
            suggestions.append("Mouse")

    return render_template("recommend.html", suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)
