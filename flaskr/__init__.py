from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for user data (replace this with a database in a real application)
users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
