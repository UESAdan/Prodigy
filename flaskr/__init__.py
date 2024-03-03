from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for user data (replace this with a database in a real application)
users = []

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Check if the username is already taken
        if any(user['username'] == username for user in users):
            return render_template('register.html', error='Username already taken')

        # Store the user data (in-memory storage for demonstration purposes)
        users.append({'username': username, 'password': password})

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)

        if user:
            # Redirect to the home page after successful login
            return render_template('index.html', username=username)
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
