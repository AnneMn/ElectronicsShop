from enum import unique
from flask import Flask, render_template, flash, redirect, url_for,session
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap 
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, form
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.core import BooleanField, SelectField
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projectdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Please log in to access this page."

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)] )
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    FirstName = StringField('FirstName', validators=[InputRequired(), Length(max=100)])
    LastName = StringField('SecondName', validators=[InputRequired(), Length(max=100)] )
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=100)] )

class Customers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return Customers.query.get(int(user_id))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer) #in shillings
    stock = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))
    manu_name = db.Column(db.String(100))
    type = db.Column(db.String(100))

    orders = db.relationship('Order_Item', backref = 'product', lazy = True)

class Contract_Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    account_number = db.Column(db.String(50))
    billing_date = db.Column(db.String(500))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reference = db.Column(db.String(5))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    status = db.Column(db.String(10))
    payment_type = db.Column(db.String(10))
    items = db.relationship('Order_Item', backref='order', lazy = True)

    def order_total(self):
        return db.session.query(db.func.sum(Order_Item.quantity * Product.price)).join(Product).filter(Order_Item.order_id == self.id).scalar() + 100

    def quantity_total(self):
        return db.session.query(db.func.sum(Order_Item.quantity)).filter(Order_Item.order_id == self.id).scalar()

class Order_Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

class reorders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pName = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    manu_name = db.Column(db.String(50))
    date = db.Column(db.String(50))
    status = db.Column(db.String(50))

class AddProduct(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    stock = IntegerField('Stock')
    manufacturer = TextAreaField('Manufacturer')
    type = TextAreaField('Type')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])

class AddCustomer(FlaskForm):
    username = StringField('Username')
    account_number = TextAreaField('Account Number')
    billing_date = TextAreaField('Billing Date')

class reorder_product(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    quantity = IntegerField('Quantity')
    manufacturer = TextAreaField('Description')
    date = TextAreaField('Date')
    status = TextAreaField('Status')

class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')

class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    address = StringField('Address')
    city = StringField('City')
    payment_type = SelectField('Payment Type', choices = [('Card', 'Card'), ('Account Number','Account Number')] )

def handle_cart():
    products = []
    grand_total = 0
    index = 0
    quantity_total = 0
    for item in session['cart']:
        product = Product.query.filter_by(id=item['id']).first()
        quantity = int(item['quantity'])
        total = quantity * product.price
        grand_total += total 
        quantity_total += quantity
        products.append({'id': product.id, 'name': product.name, 'price': product.price, 'image':product.image, 'quantity': quantity, 'total': total, 'index': index})
        index +=1
    grand_total_plus_shipping = grand_total + 100 #1000 cents
    return products, grand_total, grand_total_plus_shipping, quantity_total


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(username=form.username.data).first()
        if customer:
            if check_password_hash(customer.password, form.password.data):
                login_user(customer, remember=form.remember.data)
                flash("You are now logged in!") 
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                flash('Invalid login') 
                return redirect(url_for('login'))

    return render_template ('login.html', form=form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_customer = Customers(first_name=form.FirstName.data, last_name=form.LastName.data, email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()
        flash("You are now registed and can log in" , 'success')
        return redirect(url_for('login'))

    return render_template ('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['cart'] =[]
    session.modified =True
    flash("You have been logged out!", "success")
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route('/ourproducts')
def our_products():
    products = Product.query.all()
    return render_template('our_products.html', products=products)

@app.route('/product/<id>')
def product(id):
    product = Product.query.filter_by(id=id).first()

    form = AddToCart()

    return render_template('view-product.html', product=product, form=form)

@app.route('/quick-add/<id>')
def quick_add(id):
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append({'id': id, 'quantity': 1})
    session.modified = True

    return redirect(url_for('index'))

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
    form = AddToCart()

    if form.validate_on_submit():

        print(form.quantity.data)
        print(form.id.data)

        session ['cart'].append({'id':form.id.data, 'quantity':form.quantity.data})
        session.modified = True

    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()
    return render_template('cart.html', products=products, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total = quantity_total)

@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/checkout', methods = ['GET', 'POST'])
@login_required
def checkout():
    form = Checkout()
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()
    if form.validate_on_submit():   
        order = Order()
        form.populate_obj(order)
        order.reference = ''.join([random.choice('ABCDE') for _ in range(5)])
        order.status = 'PENDING'

        for product in products:
            order_item = Order_Item(quantity = product['quantity'], product_id= product['id'] )
            order.items.append(order_item)

        product = Product.query.filter_by(id=product['id']).update({'stock': Product.stock - product['quantity']})
        db.session.add(order)
        db.session.commit()

        
        session['cart'] =[]
        session.modified =True
        return redirect(url_for('index'))
    return render_template('checkout.html', form=form,  grand_total= grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total = quantity_total)

@app.route('/admin')
def admin():

    orders = Order.query.all()
    Reorders = reorders.query.all()
    
    return render_template('admin/index.html', admin=True, orders = orders, Reorders=Reorders)

@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))

        new_product = Product(name=form.name.data, price=form.price.data, stock=form.stock.data, description=form.description.data, image=image_url, manu_name=form.manufacturer.data, type=form.type.data)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/add-product.html', admin=True, form=form)

@app.route('/admin/add-contract-customer', methods=['GET', 'POST'])
def add_contract_customer():
   
    form = AddCustomer()
    if form.validate_on_submit():
        new_contract_customer = Contract_Customers(username=form.username.data, account_number=form.account_number.data, billing_date=form.billing_date.data)
        db.session.add(new_contract_customer)
        db.session.commit()
        return redirect(url_for('our_customers'))

    return render_template('admin/contractcustomers.html', admin=True, form=form)

@app.route('/admin/all-products', methods=['GET', 'POST'])
def all_products():
    products = Product.query.all()
    return render_template('admin/all-products.html', admin=True, products=products)

@app.route('/admin/ourcustomers', methods=['GET', 'POST'])
def our_customers():
    customers = Customers.query.all()
    contract_customers = Contract_Customers.query.all()
    return render_template('admin/ourcustomers.html', admin=True, customers = customers, contract_customers=contract_customers)

@app.route('/admin/store-inventory', methods=['GET', 'POST'])
def store_inventory():
    products = Product.query.all()
    products_in_stock = Product.query.filter(Product.stock > 0).count()
    return render_template('admin/storeinventory.html', admin=True, products=products, products_in_stock=products_in_stock)

@app.route('/admin/sales')
def sales():
    order = Order.query.all()
  
    return render_template('admin/sales.html', admin=True,   order = order)

@app.route('/admin/reorder-products', methods = ['POST', 'GET'])
def reorder():
    form = reorder_product()

    if form.validate_on_submit():

        new_reorder = reorders(pName=form.name.data, quantity=form.quantity.data, manu_name=form.manufacturer.data, date=form.date.data, status=form.status.data)

        db.session.add(new_reorder)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/reorderproducts.html', admin=True, form=form)

@app.route('/admin/delete-product/<int:id>')
def delete(id):
    product_to_delete = Product.query.get_or_404(id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('all_products'))

@app.route('/admin/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    product_to_update = Product.query.get_or_404(id)
    if request.method == "POST":
        product_to_update.name = request.form['name']
        product_to_update.price = request.form['price']
        product_to_update.stock = request.form['stock']
        product_to_update.description = request.form['description']
        product_to_update.image = request.form['image']
        product_to_update.manu_name = request.form['manufacturer']
        product_to_update.type = request.form['type']
        db.session.commit()
        return redirect (url_for('all_products'))    
    else:
        return render_template('admin/update.html', product_to_update = product_to_update, admin=True) 

@app.route('/admin/update-customer/<int:id>', methods = ['POST', 'GET'])
def update_customer(id):
    customer_to_update = Contract_Customers.query.get_or_404(id)
    if request.method == "POST":
        customer_to_update.username = request.form['username']
        customer_to_update.account_number = request.form['account number']
        customer_to_update.billing_date = request.form['billing date']
        db.session.commit()
        return redirect (url_for('our_customers'))    
    else:
        return render_template('admin/updatecustomer.html', customer_to_update = customer_to_update, admin=True) 
     
@app.route('/admin/order/<order_id>')
def order(order_id):
    order = Order.query.filter_by(id=int(order_id)).first()

    return render_template('admin/view-order.html', order = order, admin=True)


@app.route('/admin/delete-order/<int:id>')
def delete_order(id):
    order_to_delete = Order.query.get_or_404(id)
    db.session.delete(order_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete-reorder/<int:id>')
def delete_reorder(id):
    reorder_to_delete = reorders.query.get_or_404(id)
    db.session.delete(reorder_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete-customer/<int:id>')
def delete_customer(id):
    customer_to_delete = Contract_Customers.query.get_or_404(id)
    db.session.delete(customer_to_delete)
    db.session.commit()
    return redirect(url_for('our_customers'))


if __name__ == '__main__':
    app.run()
