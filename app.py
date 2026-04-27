from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "OpbP840kvNkRgRWPa36VF4UDZGZMlcQr10V-y11lEac"


# ---------------------------
# Products
# ---------------------------
PRODUCTS = [
    {"name": "Mobile", "price": 10000},
    {"name": "Laptop", "price": 50000},
    {"name": "Headphones", "price": 2000},
]


def get_product(product_name):
    for product in PRODUCTS:
        if product["name"] == product_name:
            return product
    return None


# ---------------------------
# Cart helpers
# ---------------------------
def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart


def summarize_cart(cart):
    summary = []

    for item in cart:
        found_item = False

        for row in summary:
            if row["name"] == item["name"]:
                row["quantity"] += 1
                found_item = True
                break

        if not found_item:
            summary.append({
                "name": item["name"],
                "price": item["price"],
                "quantity": 1
            })

    return summary


def calculate_total(cart):
    total = 0
    for item in cart:
        total += item["price"]
    return total


# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    cart = get_cart()
    cart_summary = summarize_cart(cart)
    total = calculate_total(cart)

    return render_template(
        "index.html",
        products=PRODUCTS,
        cart=cart_summary,
        total=total
    )


@app.route("/add", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product")
    product = get_product(product_name)

    if product:
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
        elif item["name"] == "Headphones":
            suggestions.append("Headphone Case")

    # remove duplicates while keeping order
    suggestions = list(dict.fromkeys(suggestions))

    return render_template("recommend.html", suggestions=suggestions)


@app.route("/login")
def login_page():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)