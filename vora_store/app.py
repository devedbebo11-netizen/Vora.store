from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# جدول المنتجات
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)

# جدول الأوردرات
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='جديد')

with app.app_context():
    db.create_all()

# صفحة المتجر الرئيسية لبراند Vora
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# استقبال الأوردر وتخزينه في قاعدة البيانات
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

# لوحة التحكم لمتابعة الأوردرات وإضافة منتجات
@app.route('/dashboard')
def dashboard():
    all_orders = Order.query.all()
    all_products = Product.query.all()
    return render_template('dashboard.html', orders=all_orders, products=all_products)

# إضافة منتج جديد من لوحة التحكم
@app.route('/add-product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    image_url = request.form.get('image_url')
    description = request.form.get('description')
    
    new_prod = Product(name=name, price=float(price), image_url=image_url, description=description)
    db.session.add(new_prod)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
