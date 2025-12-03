from flask import jsonify, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import app, db
from models import User
from models.cart import Cart
from models.product import Product
import os
from werkzeug.utils import secure_filename
from flask import current_app
import json
from typing import List, Dict

# ---------- LOGIN MANAGER SETUP ----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # FIXED

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(int(user_id))


# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('auth.html')


# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('Email')
        password = request.form.get('password')
        
        # Check duplicates
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)  # HASHED
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created!", "success")
        return redirect(url_for('login'))  # should login next

    return render_template('auth.html')


# ---------- LOGOUT ----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ---------- PROFILE IMAGE UPLOAD ----------

@app.route('/profile')
@login_required
def profile():
    return render_template('other-category/profile.html')

@app.route('/upload_profile', methods=['POST'])
@login_required
def upload_profile():
    if 'image' not in request.files:
        flash("No file selected.", "danger")
        return redirect(url_for('profile'))

    file = request.files['image']
    if file.filename == '':
        flash("No file selected.", "danger")
        return redirect(url_for('profile'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.root_path, "static/images/profile", filename)
    file.save(filepath)

    current_user.profile_image = filename
    db.session.commit()

    flash("Profile image updated!", "success")
    return redirect(url_for('profile'))

# ---------- ABOUT ROUTES ----------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------- CART ROUTES ----------
# ---------- CART ROUTES ----------
from flask_login import login_required, current_user

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()

    user_id = current_user.id
    product_id = data['product_id']
    name = data['name']            
    price = int(data['price'])     

    existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if existing:
        existing.quantity += 1
    else:
        new_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(new_item)

    db.session.commit()
    return {"message": "Added!"}, 200


@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    user_id = current_user.id
    product_id = data['product_id']

    item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()

    return {"message": "Item removed"}, 200

@app.route('/update-quantity', methods=['POST'])
@login_required
def update_quantity():

    data = request.get_json()
    product_id = data.get('product_id')
    action = data.get('action')
    user_id = current_user.id

    item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if not item:
        return jsonify({"ok": False, "message": "Item not found"}), 404

    if action == "plus":
        item.quantity += 1

    elif action == "minus":
        item.quantity -= 1
        if item.quantity <= 0:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"ok": True, "message": "Item removed"})

    db.session.commit()
    return jsonify({"ok": True, "message": "Quantity updated"})

@app.route('/cart')
@login_required
def cart():
    user_id = current_user.id
    cart_rows = Cart.query.filter_by(user_id=user_id).all()

    # Load product data
    with open('static/data/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    cart_items = []

    for row in cart_rows:
        for p in products:
            if int(p['id']) == int(row.product_id):
                cart_items.append({
                    "product_id": row.product_id,
                    "name": p['name'],
                    "price": p['price'],
                    "images": p.get('images', []),
                    "quantity": row.quantity,
                    "total_price": p['price'] * row.quantity
                })

    total = sum(i['total_price'] for i in cart_items)

    return render_template("cart.html", cart=cart_items, total=total)

# ---------- ORDER TRACKING ROUTES ----------
@app.route('/track-order')
def track_order():
    return render_template('track_order.html')

@app.route('/')
def home():
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except:
        products = []

    return render_template('home.html', products=products)

 
# ---------- CATEGORY ROUTES ----------
@app.route('/product')
def product():
    try:
        # Load product JSON
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
    except FileNotFoundError:
        products_data = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products_data = []

    # render template
    return render_template('product.html', products=products_data)

@app.route('/skincare')
def skincare():
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
            skincare_products = [
                p for p in products 
                if 'skincare' in [t.lower() for t in p.get('tags', [])]]

    except FileNotFoundError:
        skincare_products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        skincare_products = []
    return render_template('other-category/skincare.html', products=skincare_products)

@app.route('/makeup')
def makeup():
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
            makeup_products = [
                p for p in products 
                if 'makeup' in [t.lower() for t in p.get('tags', [])]]

    except FileNotFoundError:
        makeup_products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        makeup_products = []
    return render_template('other-category/makeup.html', products=makeup_products)


@app.route('/bestseller')
def bestseller():
    try:
        with open('static/data/bestseller.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
    except FileNotFoundError:
        products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products = []
    return render_template('other-category/bestseller.html', products=products)

@app.route('/brand/<brand_name>')
def brand(brand_name: str) -> str:
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
            brand_name_clean = brand_name.replace('-', ' ').strip().lower()

            all_brands = sorted({p.get('brand', '').strip().lower() for p in products})
            print(f"Requested brand: {brand_name_clean}")
            print(f"Available brands: {all_brands}")
            
            brand_products = [
                product for product in products 
                if product.get('brand', '').strip().lower() == brand_name_clean
                ]

    except FileNotFoundError:
        brand_products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        brand_products = []

    return render_template('other-category/brands.html', products=brand_products, brand_name=brand_name)

@app.route('/promo')
def promo():
    try:
        with open('static/data/promo.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
    except FileNotFoundError:
        products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products = []
    return render_template('other-category/promo.html', products=products)

# if app not found
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message="Page not found."), 404


# run the app 
if __name__ == '__main__':
    app.run(debug=True)
