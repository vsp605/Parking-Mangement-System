from flask import Flask, render_template, jsonify, redirect, url_for, request, flash, session, make_response
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import pdfkit
import logging

app = Flask(__name__)

# Load configuration from environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Kane@22*')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'parking_system1')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = os.getenv('SECRET_KEY', 'f894cb67a8c0b040dc8243b0864a320f')

# Initialize MySQL
mysql = MySQL(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

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

        cur.execute("SELECT message FROM notifications ORDER BY created_at DESC")
        notifications = cur.fetchall()

        cur.close()
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        user_count = 0
        notifications = []

    return render_template('index.html', user_count=user_count, notifications=notifications)

# Notifications Page
@app.route('/notifications')
def notifications():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT message, created_at FROM notifications ORDER BY created_at DESC")
        notifications = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f"Error fetching notifications: {e}")
        notifications = []

    return render_template('notifications.html', notifications=notifications)

# Admin Registration
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('admin_register'))

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO admin_users (username, email, password) VALUES (%s, %s, %s)''',
                        (username, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Admin registration successful!', 'success')
            return redirect(url_for('admin_login'))
        except Exception as e:
            logging.error(f"Error during admin registration: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('admin_register'))
    return render_template('admin_register.html')

# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin_users WHERE email = %s", (email,))
        admin_user = cur.fetchone()
        cur.close()

        if admin_user is None or not check_password_hash(admin_user[3], password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('admin_login'))

        session['admin_id'] = admin_user[0]
        session['admin_username'] = admin_user[1]
        flash('Admin login successful!', 'success')
        logging.info(f"Admin {admin_user[1]} logged in successfully.")
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please log in to access the admin dashboard.', 'danger')
        return redirect(url_for('admin_login'))
    logging.info(f"Rendering admin dashboard for admin {session.get('admin_username')}")
    return render_template('admin_dashboard.html', admin_username=session.get('admin_username'))



# User Registration
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
                filename = secure_filename(avatar_file.filename)
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar = filename

        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO users (username, first_name, last_name, mobile_number, email, password, avatar) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (username, first_name, last_name, mobile_number, email, hashed_password, avatar))
            mysql.connection.commit()
            user_id = cur.lastrowid
            cur.close()
            flash('Registration successful!', 'success')
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for('webpage'))
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user is None or not check_password_hash(user[6], password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

        session['user_id'] = user[0]
        session['username'] = user[1]
        flash('Login successful!', 'success')
        logging.info(f"User {user[1]} logged in successfully.")
        return redirect(url_for('webpage'))
    return render_template('login.html')

# Webpage after login
@app.route('/webpage')
def webpage():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    logging.info(f"Rendering webpage for user {session.get('username')}")
    return render_template('webpage.html', username=session.get('username'))

# Route for Features page
@app.route('/features')
def features():
    return render_template('features.html')

# Route for Guidelines page
@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')

# Route for Contact Us page
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/notification')
def notification():
    return render_template('notification.html')

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/pricing1')
def pricing1():
    return render_template('pricing1.html')

@app.route('/pricing2')
def pricing2():
    return render_template('pricing2.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Route to display slots for a specific location
@app.route('/slots/<location>')
def slots(location):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, location, slot_number, status FROM ParkingSlot WHERE location = %s", (location,))
        slots = cur.fetchall()
        cur.close()

        logging.debug(f"Fetched slots for location '{location}': {slots}")

        slots = list(slots)

        if len(slots) < 20:
            for i in range(len(slots), 20):
                slots.append((None, location, i + 1, 'available'))

        logging.debug(f"Final slots list for location '{location}': {slots}")

        return render_template('slots.html', location=location, slots=slots)
    except Exception as e:
        logging.error(f"Error fetching slots for location '{location}': {e}")
        flash('An error occurred while fetching slots. Please try again.', 'danger')
        return redirect(url_for('index'))

# Route to book a slot
@app.route('/book_slot', methods=['POST'])
def book_slot():
    if 'user_id' not in session:
        flash('Please log in to book a slot.', 'danger')
        return redirect(url_for('login'))
    
    slot_id = request.form['slot_id']
    slot_number = request.form['slot_number']
    location = request.form['location']
    user_id = session.get('user_id')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE ParkingSlot 
            SET status = 'booked', user_id = %s, slot_number = %s
            WHERE id = %s AND location = %s AND status = 'available'
        """, (user_id, slot_number, slot_id, location))
        mysql.connection.commit()

        if cur.rowcount == 0:
            flash('Slot is already booked or unavailable.', 'danger')
        else:
            flash('Slot booked successfully!', 'success')

        cur.close()
        return redirect(url_for('payment', slotNumber=slot_number))
    except Exception as e:
        logging.error(f"Error booking slot: {e}")
        flash('An error occurred while booking the slot. Please try again.', 'danger')
        return redirect(url_for('slots', location=location))

# Route for the payment page
@app.route('/payment')
def payment():
    slotNumber = request.args.get('slotNumber')
    return render_template('payment.html', slotNumber=slotNumber)

# Process payment
@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        plot_no = request.form.get('plotNo')
        vehicle_no = request.form.get('vehicleNo')
        vehicle_type = request.form.get('vehicleType')
        hours = int(request.form.get('hours', 0))
        amount = int(request.form.get('amount', 0))
        payment_type = request.form.get('paymentType')
        user_id = session.get('user_id')

        if not all([plot_no, vehicle_no, vehicle_type, hours, amount, payment_type]):
            return jsonify({'error': 'All fields are required!'}), 400

        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO payments (user_id, plot_no, vehicle_no, vehicle_type, hours, amount, payment_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, plot_no, vehicle_no, vehicle_type, hours, amount, payment_type)
        )
        mysql.connection.commit()
        payment_id = cur.lastrowid
        cur.close()

        return jsonify({'message': 'Payment processed successfully!', 'payment_id': payment_id, 'plot_no': plot_no, 'amount': amount, 'date': str(datetime.date.today())}), 200

    except Exception as e:
        logging.error(f"Error processing payment: {e}")
        return jsonify({'error': str(e)}), 500

# Calculate amount based on vehicle type and hours
@app.route('/calculate_amount', methods=['POST'])
def calculate_amount():
    try:
        data = request.json
        vehicle_type = data.get('vehicleType')
        hours = int(data.get('hours', 0))

        if vehicle_type not in ['2wheeler', '4wheeler']:
            return jsonify({'error': 'Invalid vehicle type!'}), 400

        if hours <= 0:
            return jsonify({'error': 'Invalid hours!'}), 400

        if vehicle_type == '2wheeler':
            amount = 20 if hours <= 2 else 20 + (hours - 2) * 10
        elif vehicle_type == '4wheeler':
            amount = 40 if hours <= 2 else 40 + (hours - 2) * 20

        return jsonify({'amount': amount}), 200

    except Exception as e:
        logging.error(f"Error calculating amount: {e}")
        return jsonify({'error': str(e)}), 500

# Route to generate bill
@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    try:
        # Retrieve data from the request
        bill_id = request.form.get('billId')
        payment_id = request.form.get('paymentId')
        slot_id = request.form.get('slotId')
        amount = request.form.get('amount')
        date = request.form.get('date')

        logging.debug(f"Generating bill for Bill ID: {bill_id}, Payment ID: {payment_id}, Slot ID: {slot_id}, Amount: {amount}, Date: {date}")

        # Fetch the username of the user associated with the payment
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT u.username 
            FROM payments p 
            JOIN users u ON p.user_id = u.id 
            WHERE p.id = %s
        """, (payment_id,))
        result = cur.fetchone()
        cur.close()

        if not result:
            raise Exception("User not found for the given payment ID")

        username = result[0]
        time = datetime.datetime.now().strftime("%H:%M:%S")

        # Render the bill template to HTML
        rendered = render_template('bill.html', bill_id=bill_id, payment_id=payment_id, slot_id=slot_id, amount=amount, date=date, time=time, username=username)

        # Path to the wkhtmltopdf binary (update this to the correct path on your system)
        wkhtmltopdf_path = os.getenv('WKHTMLTOPDF_PATH', '/usr/local/bin/wkhtmltopdf')
        if not os.path.isfile(wkhtmltopdf_path):
            raise FileNotFoundError("The wkhtmltopdf binary was not found. Check the path.")

        # Configure pdfkit with the binary path
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Generate the PDF from the rendered HTML
        pdf_content = pdfkit.from_string(rendered, False, configuration=config)

        # Create the response object to serve the PDF
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=bill_{payment_id}.pdf'

        return response

    except Exception as e:
        logging.error(f"Error generating bill: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)