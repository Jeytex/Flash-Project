from flask import Flask, redirect, render_template, request, send_file, session, url_for
import psycopg2
import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://flash_db_q6or_user:TPSwjITcZzsFyhARnGUgCMVPlarxU6Nd@dpg-d7mi23hj2pic73cbopj0-a.oregon-postgres.render.com/flash_db_q6or"
)

# ✅ Connect with SSL (required for Render)
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = "9ae4673a88e2aeb6fe63ffb2fef9b1c294e5dba90988c579ab521040b3d40779"


# ---------------- PRODUCTS ----------------
products = [
    {"name": "Mobile", "price": 10000},
    {"name": "Laptop", "price": 50000},
    {"name": "Headphones", "price": 2000},
]


# ---------------- CART LOGIC ----------------
def get_cart():
    if "cart" not in session:
        session["cart"] = []
    return session["cart"]


def save_cart(cart):
    session["cart"] = cart


def summarize_cart(cart):
    cart_summary = []

    for item in cart:
        found = False

        for summary_item in cart_summary:
            if summary_item["name"] == item["name"]:
                summary_item["quantity"] += 1
                found = True

        if not found:
            cart_summary.append({
                "name": item["name"],
                "price": item["price"],
                "quantity": 1,
            })

    return cart_summary


def calculate_total(cart):
    total = 0
    for item in cart:
        total += item["price"]
    return total


def find_product(product_name):
    for product in products:
        if product["name"] == product_name:
            return product
    return None


# ---------------- ROUTES ----------------
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

    return render_template("recommend.html", suggestions=suggestions)


@app.route("/temp67.txt")
def temp67():
    return send_file("temp67.txt", mimetype="text/plain")


@app.route("/templates")
def other_page():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)