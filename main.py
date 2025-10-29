from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import app, db
import json

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
    if 'user' in session:
        return redirect(url_for('home'))
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
    with open('static/data/products.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)
    return render_template('product.html', products=products_data)

@app.route('/skincare')
def skincare():
    return render_template('skincare.html')

@app.route('/makeup')
def makeup():
    return render_template('makeup.html')

@app.route('/bestseller')
def bestseller():
    return render_template('bestseller.html')

@app.route('/brands')
def brands():
    return render_template('brands.html')

@app.route('/promo')
def promo():
    return render_template('promo.html')


if __name__ == '__main__':
    app.run(debug=True)
