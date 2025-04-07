from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kane@22*'
app.config['MYSQL_DB'] = 'parking_system1'

# Secret key for session management
app.secret_key = 'f894cb67a8c0b040dc8243b0864a320f'

# Initialize MySQL
mysql = MySQL(app)

# Create the database and table
def init_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS parking_system")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ParkingSlot (
                id INT AUTO_INCREMENT PRIMARY KEY,
                location VARCHAR(100),
                slot_number INT,
                status ENUM('available', 'booked') DEFAULT 'available'
            )
        """)
        # Insert initial slots for Bagalkot, Navanagar, Chandana Theater
        locations = ['Bagalkot', 'Navanagar', 'Chandana Theater']
        for location in locations:
            for slot_number in range(1, 21):  # 20 slots per location
                cur.execute("INSERT INTO ParkingSlot (location, slot_number) VALUES (%s, %s)", (location, slot_number))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing the database: {e}")

@app.route('/')
def index():
    return render_template('webpage.html')

@app.route('/slots/<location>')
def slots(location):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT slot_number, status FROM ParkingSlot WHERE location = %s", (location,))
        slots = cur.fetchall()
        cur.close()
        return render_template('slots.html', location=location, slots=slots)
    except Exception as e:
        flash('Could not fetch slots. Please try again later.', 'danger')
        return redirect('/')

if __name__ == '__main__':
    init_db()  # Initialize the database and table
    app.run(debug=True)