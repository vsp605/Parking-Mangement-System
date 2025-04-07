from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kane@22*',
    'database': 'parking_system1'
}

# Connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('payment.html')  # Ensure your HTML file is named correctly

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Get form data
        plot_no = request.form.get('plotNo')
        vehicle_no = request.form.get('vehicleNo')
        vehicle_type = request.form.get('vehicleType')
        hours = int(request.form.get('hours', 0))
        amount = int(request.form.get('amount', 0))
        payment_type = request.form.get('paymentType')

        # Validate form data
        if not all([plot_no, vehicle_no, vehicle_type, hours, amount, payment_type]):
            return jsonify({'error': 'All fields are required!'}), 400

        # Insert data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO payments (plot_no, vehicle_no, vehicle_type, hours, amount, payment_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (plot_no, vehicle_no, vehicle_type, hours, amount, payment_type)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Payment processed successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
