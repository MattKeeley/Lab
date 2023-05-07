from flask import Flask, render_template, jsonify, request
import hashlib
import random
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
client = MongoClient('mongodb://localhost:27017/')
db = client['challenge']
collection = db['users']

admin_hash = ''
if collection.count_documents({}) == 0:
    print('Database is empty')
    with open('rockyou.txt', 'r', encoding='latin-1') as file:
        passwords = file.readlines()

    if passwords:
        random_password = random.choice(passwords).strip()
        admin_hash = hashlib.sha256(random_password.encode()).hexdigest()
        collection.insert_one(
            {'id': 1, 'name': 'admin', 'email': 'mkeeley@prodefense.io', 'password_hash': admin_hash})

        for i in range(1, 4):
            random_password = random.choice(passwords).strip()
            password_hash = hashlib.sha256(
                random_password.encode()).hexdigest()
            collection.insert_one(
                {'id': str(i + 1), 'name': f'user{i}', 'email': f'user{i}@prodefense.io', 'password_hash': password_hash})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/users', methods=['DELETE'])
@limiter.limit("200/hour")
def clear_users():
    collection.delete_many({})
    collection.insert_one(
        {'id': 1, 'name': 'admin', 'email': 'mkeeley@prodefense.io', 'password_hash': admin_hash})
    return jsonify("All users have been deleted (Error: Cannot delete admin user).")


@app.route('/users', methods=['POST'])
@limiter.limit("200/hour")
def create_user():
    new_user = request.get_json()
    collection.insert_one(
        {'id': collection.count_documents({}) + 1, 'name': new_user['name'], 'email': new_user['email'], 'password_hash': hashlib.sha256(new_user['password'].encode('utf-8')).hexdigest()})
    return f"User {new_user['name']} has been created."


@app.route('/users')
@limiter.limit("200/hour")
def get_users():
    sort_col = request.args.get('sort_col', default='id')
    sort_order = request.args.get('sort_order', default='asc')
    users = list(collection.find())

    sorted_users = sorted(
        users, key=lambda u: u[sort_col], reverse=(sort_order == 'dec'))

    redacted_users = []
    for user in sorted_users:
        redacted_user = user.copy()
        redacted_user['password'] = 'REDACTED'
        # Convert ObjectId to string
        redacted_user['_id'] = str(redacted_user['_id'])
        redacted_users.append(redacted_user)

    return json_util.dumps(redacted_users)


@app.route('/login', methods=['POST'])
@limiter.limit("20/hour")
def login_auth():
    username = request.form.get('username')
    password = request.form.get('password')
    user = collection.find_one({'user': username})

    if user and hashlib.sha256(password.encode()).hexdigest() == user['password_hash']:
        print('Login successful')
        return 'Login successful', 200
    else:
        print('Invalid credentials')
        return 'Invalid credentials', 403


if __name__ == '__main__':
    app.run(debug=False)
