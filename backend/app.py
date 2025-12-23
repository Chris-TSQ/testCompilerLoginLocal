from flask import Flask, request, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    success, message = database.create_user(username, email, password)
    
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = database.verify_user(username, password)
    
    if user is None:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token, username = database.create_session(user['id'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'username': username
    }), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.replace('Bearer ', '')
    database.delete_session(token)
    
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/verify', methods=['GET'])
def verify():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.replace('Bearer ', '')
    user = database.verify_session(token)
    
    if user is None:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    return jsonify({
        'username': user['username'],
        'email': user['email']
    }), 200

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True, port=5000)