from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kane@22*'
app.config['MYSQL_DB'] = 'parking_system1'

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Secret key for sessions and flash messages
app.secret_key = 'f894cb67a8c0b040dc8243b0864a320f'

# Initialize MySQL
mysql = MySQL(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home Page
@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        cur.close()
    except Exception as e:
        print(f"Error fetching user count: {e}")
        user_count = 0
    return render_template('index.html', user_count=user_count)

# Features Page
@app.route('/features')
def features():
    return render_template('features.html')

# User Registration and Login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        mobile_number = request.form['mobileNumber']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        avatar = None

        if 'avatarUpload' in request.files:
            avatar_file = request.files['avatarUpload']
            if avatar_file and allowed_file(avatar_file.filename):
                filename = avatar_file.filename
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar = filename

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                '''INSERT INTO users (username, first_name, last_name, mobile_number, email, password, avatar) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (username, first_name, last_name, mobile_number, email, hashed_password, avatar)
            )
            mysql.connection.commit()
            cur.close()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error during registration: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[6], password):  # user[6] is the hashed password
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('webpage'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/webpage')
def webpage():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    return render_template('webpage.html', username=session.get('username'))

# Route to display slots for a specific location
@app.route('/slots/<location>', methods=['GET', 'POST'])
def slots(location):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM parking_slots1 WHERE location = %s", (location,))
        slots = cur.fetchall()
        cur.close()

        # Ensure at least 20 slots are displayed
        if len(slots) < 20:
            for i in range(len(slots) + 1, 21):
                slots.append((None, location, i, 'available'))

        if request.method == 'POST':
            slot_id = request.form.get('slot_id')
            try:
                cur = mysql.connection.cursor()
                cur.execute(
                    "UPDATE parking_slots1 SET status = 'booked', user_id = %s WHERE slot_id = %s AND location = %s AND status = 'available'",
                    (session['user_id'], slot_id, location)
                )
                mysql.connection.commit()
                cur.close()
                flash('Slot booked successfully!', 'success')
                return redirect(url_for('slots', location=location))
            except Exception as e:
                print(f"Error booking slot: {e}")
                flash('Error booking the slot. Please try again.', 'danger')

        return render_template('slots.html', location=location, slots=slots)
    except Exception as e:
        print(f"Error fetching slots: {e}")
        flash('An error occurred while fetching slots. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
