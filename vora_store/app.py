from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# ضبط مسارات الـ templates والـ static داخل مجلد vora_store
app = Flask(__name__, template_folder='templates', static_folder='static')

# إعداد قاعدة البيانات SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# تعريف جدول المنتجات
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

# تعريف جدول الطلبات
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    items = db.Column(db.Text, nullable=False)

# إنشاء الجداول تلقائياً
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    items = request.form.get('items')
    
    new_order = Order(customer_name=name, phone=phone, address=address, items=items)
    db.session.add(new_order)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image_url = request.form.get('image_url')
        
        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    products = Product.query.all()
    orders = Order.query.all()
    return render_template('dashboard.html', products=products, orders=orders)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)