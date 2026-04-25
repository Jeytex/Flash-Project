from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret"

# Fake database
products = [
    {"name": "Mobile", "price": 10000},
    {"name": "Laptop", "price": 50000},
    {"name": "Headphones", "price": 2000}
]

def get_cart():
    return session.get("cart", [])

def save_cart(cart):
    session["cart"] = cart

def cart_summary(cart):
    summary = {}
    for item in cart:
        name = item["name"]
        if name not in summary:
            summary[name] = {"name": name, "price": item["price"], "quantity": 0}
        summary[name]["quantity"] += 1
    return list(summary.values())

def cart_total(cart):
    return sum(item["price"] for item in cart)

@app.route("/")
def home():
    cart = get_cart()
    return render_template(
        "index.html",
        products=products,
        cart=cart_summary(cart),
        total=cart_total(cart)
    )

@app.route("/add", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product")
    cart = get_cart()

    for p in products:
        if p["name"] == product_name:
            cart.append(p)
            break

    save_cart(cart)
    return redirect(url_for("home"))

@app.route("/clear", methods=["POST"])
def clear_cart():
    save_cart([])
    return redirect(url_for("home"))

@app.route("/recommend")
def recommend():
    suggestions = []
    for item in get_cart():
        if item["name"] == "Mobile":
            suggestions.append("Charger")
        if item["name"] == "Laptop":
            suggestions.append("Mouse")

    return render_template("recommend.html", suggestions=suggestions)

if __name__ == "__main__":
    app.run()