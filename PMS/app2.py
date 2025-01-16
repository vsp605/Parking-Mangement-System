from flask import Flask, render_template, jsonify, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kane%4022%2A@localhost/parking_system1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class ParkingSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    slot_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')  # available or booked

# Route: Display Main Page with Parking Locations
@app.route('/')
def index():
    locations = ['Hanuman Temple BGK', 'Sector 25 Nava Nagar BGK', 'near Nava Nagar Bustand Road']
    return render_template('webpage.html', locations=locations)

# Route: Render Slot Page for Selected Location
@app.route('/slots/<location>')
def slots(location):
    slots = ParkingSlot.query.filter_by(location=location).all()
    max_slots = 20
    # Pad the list to always show 20 slots
    for i in range(len(slots) + 1, max_slots + 1):
        slots.append(ParkingSlot(id=None, location=location, slot_number=i, status='available'))
    return render_template('slot.html', location=location, slots=slots)

# Route: Parking Prices Page
@app.route('/pricing.html')
def pricing():
    return render_template('pricing.html')

@app.route('/pricing1.html')
def pricing1():
    return render_template('pricing1.html')

@app.route('/pricing2.html')
def pricing2():
    return render_template('pricing2.html')

# API Route: Book a Parking Slot
@app.route('/api/book/<int:slot_id>', methods=['POST'])
def book_slot(slot_id):
    slot = ParkingSlot.query.get(slot_id)
    if slot and slot.status == 'available':
        slot.status = 'booked'
        db.session.commit()
        return jsonify({'message': 'Slot booked successfully!'})
    return jsonify({'message': 'Slot already booked or invalid.'}), 400

# Route to handle slot booking from the web interface
@app.route('/book/<int:slot_id>', methods=['POST'])
def book_slot_web(slot_id):
    slot = ParkingSlot.query.get(slot_id)
    if slot and slot.status == 'available':
        slot.status = 'booked'
        db.session.commit()
        # Redirect to payment page after booking
        return redirect(url_for('payment'))
    # Redirect to the homepage if booking fails
    flash('Slot already booked or invalid.', 'danger')
    return redirect(url_for('index'))

# Route to render the payment page
@app.route('/payment.html')
def payment():
    return render_template('payment.html')

# Route to process the payment
@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Safely fetch form data
    plot_no = request.form.get('plotNo')
    vehicle_no = request.form.get('vehicleNo')
    vehicle_type = request.form.get('vehicleType')
    hours = request.form.get('hours')
    amount = request.form.get('amount')
    payment_type = request.form.get('paymentType')

    # Log the details to the console for now
    print(f'Plot No: {plot_no}')
    print(f'Vehicle No: {vehicle_no}')
    print(f'Vehicle Type: {vehicle_type}')
    print(f'Hours: {hours}')
    print(f'Amount: {amount}')
    print(f'Payment Type: {payment_type}')

    # Redirect to the home page after processing
    flash('Payment processed successfully!', 'success')
    return redirect(url_for('index'))

# Initialize Database and Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    app.run(debug=True)