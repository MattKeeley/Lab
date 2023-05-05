from flask import Flask, render_template, jsonify, request
import hashlib

app = Flask(__name__)

# Pretend this is a databse :P
users = [
    {'id': 1, 'name': 'admin', 'email': 'admin@example.com',
     'password': 'dbfd43b661440a7725c23e277c62e33277acfbdf7331b56fc5545b928894416d'},
    {'id': 2, 'name': 'Matt', 'email': 'matt@example.com',
        'password': '50eb299b46fe70fb31b22d195410c0c2b6b959a8beebd8c2c080f428b90b591f'},
    {'id': 3, 'name': 'Ryan', 'email': 'ryan@example.com',
        'password': '4062a90a69c6a9007cbb627030e7ee67948cc842632d2c6e1c0cf75c087f0e20'},
    {'id': 4, 'name': 'Nathan', 'email': 'nathan@example.com',
        'password': 'a85a433586c7cc7c7a3c0a1b85f9ce78b5c06a2b5af926a4bf1c96fd37d408fc'}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['DELETE'])
def clear_users():
    global users
    users = [
        {'id': 1, 'name': 'admin', 'email': 'admin@example.com',
         'password': 'dbfd43b661440a7725c23e277c62e33277acfbdf7331b56fc5545b928894416d'}]
    return jsonify("users deleted")


@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    new_user['id'] = len(users) + 1
    password = new_user['password'].encode('utf-8')
    hashed_password = hashlib.sha256(password).hexdigest()
    new_user['password'] = hashed_password
    users.append(new_user)
    return jsonify(new_user)


@app.route('/users')
def get_users():
    sort_col = request.args.get('sort_col', default='id')
    sort_order = request.args.get('sort_order', default='asc')

    sorted_users = sorted(
        users, key=lambda u: u[sort_col], reverse=(sort_order == 'dec'))

    for user in sorted_users:
        user['password'] = 'REDACTED'
    return jsonify(sorted_users)


if __name__ == '__main__':
    app.run(debug=False)
