from flask import render_template, redirect, url_for, request, session, flash
from config import app, db
import json
from typing import List, Dict

users = {"admin": "12345"} # Simple in-memory user store

# ---------- MAIN ROUTES ----------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/auth')
def auth():
    try:
        if 'user' in session:
            return redirect(url_for('home'))
    except Exception as e:
        print(f"An error occurred: {e}")

    return render_template('auth.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['user'] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("❌ Invalid username or password!", "error")
            return redirect(url_for('auth'))

    return render_template('auth.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if username in users:
        flash('⚠️ User already exists! Please choose another username.', 'error')
        return redirect(url_for('auth'))

    users[username] = password
    session['user'] = username
    flash('✅ Registration successful!', 'success')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

# ---------- CATEGORY ROUTES ----------
@app.route('/product')
def product():
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
    except FileNotFoundError:
        products_data = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products_data = []

    return render_template('product.html', products=products_data)

@app.route('/skincare')
def skincare():
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products : List[Dict[str,str]] = json.load(f) 
    except FileNotFoundError:
        products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products = []

    return render_template('skincare.html', products=products)

@app.route('/makeup')
def makeup():
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
    except FileNotFoundError:
        products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products = []
    return render_template('makeup.html', products=products)

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
def brand(brand_name: str):
    try:
        with open('static/data/products.json', 'r', encoding='utf-8') as f:
            products: List[Dict[str, str]] = json.load(f)
            brand_products = [product for product in products if product.get('brand') == brand_name]
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
