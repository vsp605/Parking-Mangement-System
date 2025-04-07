import secrets
from flask import Flask, session, redirect, url_for, flash

app = Flask(__name__)

# Generate a secure secret key
secret_key = secrets.token_hex(24)

# Print the secret key for verification (for debugging only; remove in production!)
print(f"Generated secret key: {secret_key}")

# Set the secret key for the Flask application
app.secret_key = 'f894cb67a8c0b040dc8243b0864a320f'

# Example route
@app.route('/')
def home():
    return "Secure Flask Application"

# Route to set a value in the session
@app.route('/set_session/<value>')
def set_session(value):
    session['key'] = value
    flash('Session value set successfully!', 'success')
    return redirect(url_for('get_session'))

# Route to get the value from the session
@app.route('/get_session')
def get_session():
    value = session.get('key', 'Not set')
    return f'Session value: {value}'

# Route to clear the session value
@app.route('/clear_session')
def clear_session():
    session.pop('key', None)
    flash('Session value cleared!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
