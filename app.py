from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key="simple-secret-key"


PRODUCTS = [

{"id":"laptop","name":"ASUS Vivobook","price":45000,"image":"images/laptop1.jpg"},
{"id":"phone","name":"Samsung Galaxy S26","price":18000,"image":"images/mobile1.jpg"},
{"id":"camera","name":"Sony AES Digital Camera","price":32000,"image":"images/camera1.jpg"},
{"id":"controller","name":"PS5 Controller","price":3500,"image":"images/ps5controller.jpg"},
{"id":"charger","name":"65W Type C Charger","price":900,"image":"images/mobilecharger.jpg"},
{"id":"tv","name":"TCL 75inch LED","price":28000,"image":"images/tv.jpg"},

{"id":"camera_2","name":"Kodak Digital Camera","price":42000,"image":"images/camera2.jpg."},
{"id":"camera_lens","name":"Camera Lens","price":21000,"image":"images/cameralens.jpg"},
{"id":"camera_pod","name":"Tripod for DSLR Cameras","price":12000,"image":"images/camerapod.jpg"},

{"id":"ps5","name":"PS5","price":48000,"image":"images/ps5.jpg"},
{"id":"laptop2","name":"Macbook Air M4","price":82000,"image":"images/laptop2.jpg"},
{"id":"laptop3","name":"Lenovo Legion","price":111400,"image":"images/laptop3.jpg"},

]


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):

        if not session.get("logged_in"):
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return check


def find_product(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return p
    return None


def get_cart():
    c = session.get("cart")
    if not c:
        c = {}
    return c


def save_cart(c):
    session["cart"] = c


def get_cart_items():
    items = []
    cart = get_cart()

    for p in PRODUCTS:
        q = cart.get(p["id"],0)

        if q!=0:
            item = {}
            item.update(p)
            item["quantity"] = q
            item["total"] = p["price"] * q
            items.append(item)

    return items


def get_recommendations(pid, limit=2):
    rec = []
    for p in PRODUCTS:
        if p["id"] != pid:
            rec.append(p)

    return rec[:limit]


@app.route("/", methods=["GET","POST"])
def login():

    if session.get("logged_in"):
        return redirect("/products")

    err = None

    if request.method=="POST":

        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()

        if u and p:
            session["logged_in"]=True
            session["username"]=u

            if "cart" not in session:
                session["cart"]={}

            return redirect("/products")

        else:
            err = "Enter a username and password."

    return render_template("login.html", error=err)


@app.route("/login", methods=["GET","POST"])
def login_old():
    return login()


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/products")
@login_required
def products():
    return render_template("products.html", products=PRODUCTS)


@app.route("/add", methods=["POST"])
@login_required
def add():

    pid = request.form.get("product")

    if find_product(pid):
        cart = get_cart()

        if pid in cart:
            cart[pid]+=1
        else:
            cart[pid]=1

        save_cart(cart)

    return redirect("/products")


@app.route("/remove", methods=["POST"])
@login_required
def remove():

    pid = request.form.get("product")
    cart = get_cart()

    if pid in cart:
        if cart[pid] > 1:
            cart[pid] = cart[pid] - 1
        else:
            cart.pop(pid,None)

    save_cart(cart)

    return redirect("/cart")


@app.route("/cart")
@login_required
def cart():

    items = get_cart_items()

    for i in items:
        i["recommendations"] = get_recommendations(i["id"])

    total = 0
    for i in items:
        total += i["total"]

    return render_template("cart.html", cart_items=items, total=total)


@app.route("/clear", methods=["POST"])
@login_required
def clear():
    save_cart({})
    return redirect("/cart")


# random route lol
@app.route("/shrek")
def shrek():
    return render_template("chatbot.html")


if __name__=="__main__":
    app.run(debug=True)