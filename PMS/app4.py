from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kane@22*',
    'database': 'parking_system1'
}

# Route for the bill form
@app.route('/')
def bill_form():
    return render_template('bill.html')  # Render the bill form

# Route to handle form submission
@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get form data
        bill_id = request.form.get('billId')
        payment_id = request.form.get('paymentId')
        slot_id = request.form.get('slotId')
        amount = request.form.get('amount')
        date = request.form.get('date')

        # Debug: Print received data
        print(f"Received Data: {bill_id}, {payment_id}, {slot_id}, {amount}, {date}")

        # SQL query to insert data into the Bill table
        query = """
        INSERT INTO Bill (bill_id, payment_id, slot_id, amount, bill_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (bill_id, payment_id, slot_id, amount, date))
        conn.commit()  # Commit the transaction

        # Close the database connection
        cursor.close()
        conn.close()

        # Return success response
        return jsonify({'message': 'Bill generated successfully!', 'bill_id': bill_id})

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")  # Debug: Print MySQL error
        return jsonify({'error': str(err)})

    except Exception as e:
        print(f"General Error: {e}")  # Debug: Print general error
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
