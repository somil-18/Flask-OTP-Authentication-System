from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://@DESKTOP-F91EBN7/nest?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rommie152@gmail.com'
app.config['MAIL_PASSWORD'] = 'busy mbky fvzv gybr'
app.config['MAIL_DEFAULT_SENDER'] = 'rommie152@gmail.com'
mail = Mail(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def _repr_(self):
        return f"<User {self.email}>"

# OTP Generator
def generate_otp():
    return str(random.randint(100000, 999999))

# Routes

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Send OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    otp = generate_otp()
    session['otp'] = otp
    session['email'] = email

    try:
        msg = Message('Your OTP Code', recipients=[email])
        msg.body = f'Your OTP code is: {otp}. It is valid for 5 minutes.'
        mail.send(msg)
        return jsonify({'message': f'OTP sent to {email}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    user_otp = data.get('otp')

    if 'otp' not in session:
        return jsonify({'error': 'No OTP found. Please request a new OTP.'}), 400

    if user_otp == session['otp']:
        return jsonify({'message': 'OTP verified successfully! ✅'}), 200
    else:
        return jsonify({'error': 'Invalid OTP. ❌'}), 400

# Resend OTP
@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    new_otp = generate_otp()
    session['otp'] = new_otp

    try:
        msg = Message('Resend OTP Code', recipients=[email])
        msg.body = f'Your new OTP code is: {new_otp}. It is valid for 5 minutes.'
        mail.send(msg)
        return jsonify({'message': 'OTP resent successfully! ✅'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists! ❌'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session.pop('otp', None)

    return jsonify({'message': 'Signup successful! ✅', 'redirect': '/main'}), 200



#  Login Route
@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = data.get(email)

    if user and check_password_hash(user['password'], password):
        session['email'] = email  
        return jsonify({'message': 'Login successful! ✅', 'success': True}), 200
    else:
        return jsonify({'error': 'Invalid email or password ❌', 'success': False}), 400


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/rent')
def rent_page():
    if 'email' not in session:
        return redirect(url_for('signup'))
    return render_template('rent.html')

@app.route('/list')
def list_page():
    if 'email' not in session:
        return redirect(url_for('signup'))
    return render_template('list.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/about')
def about_page():
    return render_template('about.html')


# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


    