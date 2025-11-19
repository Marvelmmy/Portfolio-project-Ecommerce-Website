from flask import render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
from typing import List, Dict, DefaultDict
from collections import defaultdict
from config import app
import models
from models.user import User
from models.product import Product

users = {"admin": "12345"} # Simple in-memory user store

# ---------- LOGIN MANAGER SETUP ----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # handle login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = models.User.query.filter_by(username=username).first()
        if user and user.password == password:  # (hash this later!)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    # render login template
    return render_template('auth.html')

# logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# ---------- MAIN ROUTES ----------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    price = int(request.form.get('price'))

    cart = session.get('cart', [])
    found = False

    for item in cart:
        if item ['product_id'] == product_id:
            item['quantity'] += 1
            found = True
            break

    if not found:
        cart.append({'product_id': product_id, 'name': name, 'price': price, 'quantity': 1})

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/track-order')
def track_order():
    return render_template('track_order.html')

@app.route('/')
def home():
    return render_template('home.html')

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
    return render_template('promo.html')

# if app not found
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message="Page not found."), 404


# run the app 
if __name__ == '__main__':
    app.run(debug=True)
