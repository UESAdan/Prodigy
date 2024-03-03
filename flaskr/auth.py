import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

from urllib.request import urlopen
from bs4 import BeautifulSoup
import openai
import nltk
import openai
from googlesearch import search

def search(age = 5, location = "", passion = ""):
    openai.api_key = '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'

    messages = [ {"role": "system", "content":  
                "You are a intelligent assistant."} ] 

    message = "Give me 5 programs for" + age + "year olds in " + location + "for a passion for " + passion +", and give exact organizations, programs, clubs, and opportunities. Start a new line for every program, give me white space, give the information in a concise manner. But keep the url. Return the string with new lines for each program and url."
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 
        reply = chat.choices[0].message.content 
        return(f"{reply}") 

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']


        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required'

      
        if error is None:
            try:
                db.execute(
                     "INSERT INTO users (username, email, password) VALUES (?,?,?)",
                     (username,email,generate_password_hash(password)),
                 )
                db.commit()

            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))
            
        flash(error)

        # Check if the username is already taken

        # Redirect to login page after successful registration
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()

        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('pages.home'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE user_id = ?', (user_id,)
        ).fetchone()

@bp.route('/register_child', methods =['GET', 'POST'])
def register_child():
    if request.method == 'POST':
        child_name = request.form['name']
        child_profession = request.form['profession']
        child_location = request.form['location']
        child_age = request.form['age']
        
        # Assuming you store the logged-in user's ID in session['user_id']
        user_id = session.get('user_id')
        
        db = get_db()
        error = None

        if not user_id:
            error = "User must be logged in to register a child."
        elif not child_name:
            error = "Child's name is required."
        elif not child_profession:
            error = "Child's profession is required."
        elif not child_location:
            error = "Child's location is required."
        elif not child_age:
            error = "Child's age is required."
        else:
            try:
                programs = search(child_age, child_location, child_profession)
                db.execute(
                    "INSERT INTO kids (user_id, name, profession, location, programs, age) VALUES (?,?,?,?,?,?)",
                    (user_id, child_name, child_profession, child_location, programs, child_age),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Child {child_name} with profession {child_profession} is already registered for this user."
            else:
                return redirect(url_for('pages.profile'))  

        if error:
            flash(error)

    # If GET request or there is an error, show the registration page again
    return render_template('auth/register_child.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view