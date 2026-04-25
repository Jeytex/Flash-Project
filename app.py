from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Fake database
products = [
    {"name": "Mobile", "price": 10000},
    {"name": "Laptop", "price": 50000},
    {"name": "Headphones", "price": 2000}
]

cart = []

@app.route("/")
def home():
    return render_template("index.html", products=products, cart=cart)

@app.route("/add", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product")
    
    for p in products:
        if p["name"] == product_name:
            cart.append(p)

    return redirect(url_for("home"))

@app.route("/recommend")
def recommend():
    suggestions = []
    
    for item in cart:
        if item["name"] == "Mobile":
            suggestions.append("Charger")
        if item["name"] == "Laptop":
            suggestions.append("Mouse")

    return render_template("recommend.html", suggestions=suggestions)

if __name__ == "__main__":
    app.run()