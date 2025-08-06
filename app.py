from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import re
from datetime import datetime
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    reg_number = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    products = db.relationship('Product', backref='seller', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='messages')

# Helper Functions
def validate_reg_number(reg_number):
    pattern = r'^[A-Z]\d{6}[A-Z]$'
    return re.match(pattern, reg_number) is not None

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_available=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.title.contains(search) | Product.description.contains(search))
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=8, error_out=False
    )
    
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    breadcrumbs = [{'name': 'Home', 'url': url_for('index')}]
    if category:
        breadcrumbs.append({'name': category, 'url': url_for('index', category=category)})
    
    return render_template('index.html', products=products, categories=categories, 
                         current_category=category, search=search, breadcrumbs=breadcrumbs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            identifier = request.form.get('identifier', '').strip()
            password = request.form.get('password', '')
            
            if not identifier or not password:
                flash('Please fill in all fields.', 'error')
                return render_template('login.html')
            
            # Check if identifier is email or reg number
            user = None
            if '@' in identifier:
                user = User.query.filter_by(email=identifier).first()
            else:
                if not validate_reg_number(identifier.upper()):
                    flash('Invalid registration number format. Use format: H200000A', 'error')
                    return render_template('login.html')
                user = User.query.filter_by(reg_number=identifier.upper()).first()
            
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials. Please try again.', 'error')
                
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
            app.logger.error(f'Login error: {str(e)}')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            reg_number = request.form.get('reg_number', '').strip().upper()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validation
            if not all([name, password, confirm_password]):
                flash('Please fill in all required fields.', 'error')
                return render_template('register.html')
            
            if not email and not reg_number:
                flash('Please provide either email or registration number.', 'error')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('register.html')
            
            if reg_number and not validate_reg_number(reg_number):
                flash('Invalid registration number format. Use format: H200000A', 'error')
                return render_template('register.html')
            
            # Check for existing users
            if email and User.query.filter_by(email=email).first():
                flash('Email already registered.', 'error')
                return render_template('register.html')
            
            if reg_number and User.query.filter_by(reg_number=reg_number).first():
                flash('Registration number already registered.', 'error')
                return render_template('register.html')
            
            # Create new user
            user = User(
                name=name,
                email=email if email else None,
                reg_number=reg_number if reg_number else None,
                password_hash=generate_password_hash(password)
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            app.logger.error(f'Registration error: {str(e)}')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('index')},
        {'name': product.category, 'url': url_for('index', category=product.category)},
        {'name': product.title, 'url': ''}
    ]
    return render_template('product_detail.html', product=product, breadcrumbs=breadcrumbs)

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_product():
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', '')
            category = request.form.get('category', '').strip()
            condition = request.form.get('condition', '').strip()
            image_url = request.form.get('image_url', '').strip()
            
            if not all([title, description, price, category, condition]):
                flash('Please fill in all required fields.', 'error')
                return render_template('sell.html')
            
            try:
                price = float(price)
                if price <= 0:
                    raise ValueError()
            except ValueError:
                flash('Please enter a valid price.', 'error')
                return render_template('sell.html')
            
            product = Product(
                title=title,
                description=description,
                price=price,
                category=category,
                condition=condition,
                image_url=image_url if image_url else '/placeholder.svg?height=300&width=300',
                seller_id=session['user_id']
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('Product listed successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while listing the product. Please try again.', 'error')
            app.logger.error(f'Sell product error: {str(e)}')
    
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('index')},
        {'name': 'Sell Product', 'url': ''}
    ]
    return render_template('sell.html', breadcrumbs=breadcrumbs)

@app.route('/chat/<int:product_id>')
@login_required
def chat(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.seller_id == session['user_id']:
        flash('You cannot message yourself about your own product.', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    messages = Message.query.filter_by(product_id=product_id).filter(
        ((Message.sender_id == session['user_id']) & (Message.receiver_id == product.seller_id)) |
        ((Message.sender_id == product.seller_id) & (Message.receiver_id == session['user_id']))
    ).order_by(Message.timestamp.asc()).all()
    
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('index')},
        {'name': product.title, 'url': url_for('product_detail', product_id=product_id)},
        {'name': 'Chat', 'url': ''}
    ]
    
    return render_template('chat.html', product=product, messages=messages, breadcrumbs=breadcrumbs)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        product = Product.query.get_or_404(product_id)
        
        if product.seller_id == session['user_id']:
            return jsonify({'error': 'Cannot message yourself'}), 400
        
        message = Message(
            sender_id=session['user_id'],
            receiver_id=product.seller_id,
            product_id=product_id,
            content=content
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': {
                'content': content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'sender_name': session['user_name']
            }
        })
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Send message error: {str(e)}')
        return jsonify({'error': 'Failed to send message'}), 500

@app.route('/my_products')
@login_required
def my_products():
    products = Product.query.filter_by(seller_id=session['user_id']).order_by(Product.created_at.desc()).all()
    breadcrumbs = [
        {'name': 'Home', 'url': url_for('index')},
        {'name': 'My Products', 'url': ''}
    ]
    return render_template('my_products.html', products=products, breadcrumbs=breadcrumbs)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message='Internal server error'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
