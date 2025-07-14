import json
import uuid
import logging
from flask import Flask, render_template, jsonify, request, send_from_directory, session, redirect, url_for
from hardware.camera_control import scan_label
from ocr.expiry_ocr import extract_expiry
from hardware.led_control import set_led_status
from notifications.sms_sender import send_sms
import datetime
import os

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = 'smartshelf_secret_key'  # For session management

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), 'products.json')
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

# --- Persistent Storage Helpers ---
def load_products():
    try:
        if not os.path.exists(PRODUCTS_FILE):
            return []
        with open(PRODUCTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load products: {e}")
        return []

def save_products(products):
    try:
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(products, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save products: {e}")

def load_users():
    try:
        if not os.path.exists(USERS_FILE):
            return []
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load users: {e}")
        return []

def update_product_status(products):
    today = datetime.date.today()
    for prod in products:
        try:
            exp = datetime.datetime.strptime(prod["expiry"], "%Y-%m-%d").date()
            if exp < today:
                prod["status"] = "expired"
            elif (exp - today).days <= 7:
                prod["status"] = "near"
            else:
                prod["status"] = "safe"
        except Exception as e:
            prod["status"] = "unknown"
            logging.error(f"Invalid expiry date for product {prod.get('name')}: {e}")

def is_logged_in():
    return session.get('user') is not None

def validate_product_data(data):
    if not isinstance(data, dict):
        return False, 'Invalid data format.'
    name = data.get('name')
    expiry = data.get('expiry')
    if not name or not isinstance(name, str):
        return False, 'Product name is required.'
    try:
        datetime.datetime.strptime(expiry, "%Y-%m-%d")
    except Exception:
        return False, 'Expiry date must be in YYYY-MM-DD format.'
    return True, ''

# --- Auth Routes ---
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user'] = username
                logging.info(f"User {username} logged in.")
                return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed.'}), 500

@app.route("/logout", methods=["POST"])
def logout():
    user = session.pop('user', None)
    logging.info(f"User {user} logged out.")
    return jsonify({'success': True})

# --- Routes ---
@app.route("/")
def landing():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/products", methods=["GET"])
def api_products():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        products = load_products()
        update_product_status(products)
        save_products(products)
        return jsonify({"products": products})
    except Exception as e:
        logging.error(f"Failed to get products: {e}")
        return jsonify({'error': 'Failed to get products.'}), 500

@app.route("/api/products", methods=["POST"])
def api_create_product():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    valid, msg = validate_product_data(data)
    if not valid:
        return jsonify({'error': msg}), 400
    try:
        products = load_products()
        new_product = {
            "id": str(uuid.uuid4()),
            "name": data.get("name", "Unnamed Product"),
            "expiry": data.get("expiry", "2099-12-31"),
            "status": "safe"
        }
        products.append(new_product)
        update_product_status(products)
        save_products(products)
        logging.info(f"Product created: {new_product}")
        return jsonify(new_product), 201
    except Exception as e:
        logging.error(f"Failed to create product: {e}")
        return jsonify({'error': 'Failed to create product.'}), 500

@app.route("/api/products/<pid>", methods=["PUT"])
def api_update_product(pid):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    valid, msg = validate_product_data(data)
    if not valid:
        return jsonify({'error': msg}), 400
    try:
        products = load_products()
        for prod in products:
            if prod["id"] == pid:
                prod["name"] = data.get("name", prod["name"])
                prod["expiry"] = data.get("expiry", prod["expiry"])
                update_product_status(products)
                save_products(products)
                logging.info(f"Product updated: {prod}")
                return jsonify(prod)
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logging.error(f"Failed to update product: {e}")
        return jsonify({'error': 'Failed to update product.'}), 500

@app.route("/api/products/<pid>", methods=["DELETE"])
def api_delete_product(pid):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        products = load_products()
        new_products = [prod for prod in products if prod["id"] != pid]
        if len(new_products) == len(products):
            return jsonify({'error': 'Product not found'}), 404
        save_products(new_products)
        logging.info(f"Product deleted: {pid}")
        return ("", 204)
    except Exception as e:
        logging.error(f"Failed to delete product: {e}")
        return jsonify({'error': 'Failed to delete product.'}), 500

@app.route("/api/products/<pid>/check", methods=["POST"])
def mark_checked(pid):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        products = load_products()
        for prod in products:
            if prod["id"] == pid:
                prod["status"] = "safe"
        save_products(products)
        logging.info(f"Product marked as checked: {pid}")
        return ("", 204)
    except Exception as e:
        logging.error(f"Failed to mark product as checked: {e}")
        return jsonify({'error': 'Failed to mark product as checked.'}), 500

@app.route("/api/scan", methods=["POST"])
def api_scan():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        products = load_products()
        if products:
            image = scan_label()
            expiry_date = extract_expiry(image)
            products[0]["expiry"] = expiry_date
            update_product_status(products)
            save_products(products)
            logging.info(f"Product scanned and expiry updated: {products[0]}")
        return ("", 204)
    except Exception as e:
        logging.error(f"Failed to scan product: {e}")
        return jsonify({'error': 'Failed to scan product.'}), 500

@app.route("/api/alerts", methods=["POST"])
def api_alerts():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        products = load_products()
        for prod in products:
            if prod["status"] in ["expired", "near"]:
                send_sms(f"Alert: {prod['name']} expires on {prod['expiry']}")
        logging.info("Alerts sent for expired/near-expiry products.")
        return ("", 204)
    except Exception as e:
        logging.error(f"Failed to send alerts: {e}")
        return jsonify({'error': 'Failed to send alerts.'}), 500

if __name__ == "__main__":
    # If products.json does not exist, create with demo data
    if not os.path.exists(PRODUCTS_FILE):
        demo_products = [
            {"id": "1", "name": "Milk", "expiry": "2025-12-31", "status": "safe"},
            {"id": "2", "name": "Yogurt", "expiry": "2024-07-15", "status": "near"},
            {"id": "3", "name": "Cheese", "expiry": "2024-06-01", "status": "expired"}
        ]
        save_products(demo_products)
    # If users.json does not exist, create with demo user
    if not os.path.exists(USERS_FILE):
        demo_users = [
            {"username": "admin", "password": "admin123"}
        ]
        with open(USERS_FILE, 'w') as f:
            json.dump(demo_users, f, indent=2)
    app.run(debug=True)
