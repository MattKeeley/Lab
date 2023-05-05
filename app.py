from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Pretend this is a databse :P
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'password': 'bbb'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'password': 'aaa'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com', 'password': 'ccc'}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        'id': len(users) + 1,
        'name': request.form['name'],
        'email': request.form['email']
    }
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
    app.run(debug=True)
