from flask import (
    Blueprint, flash, g, redirect, render_template, session, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('pages', __name__)

def create_app():
    app = ...
    # existing code omitted

    from . import pages
    app.register_blueprint(pages.bp)
    app.add_url_rule('/', endpoint='index')

    return app

@bp.route('/', methods =['GET', 'POST'])
def index():
    return render_template('pages/index.html')#, posts=posts)

@bp.route('/home', methods =['GET', 'POST'])
def home():
    return render_template('pages/home.html')#, posts=posts)

@bp.route('/profile', methods =['GET', 'POST'])
def profile():
    db = get_db()
    user_id = session.get('user_id')

    posts = db.execute(
        'SELECT name,profession,age FROM kids WHERE user_id = ?', (user_id,)
    ).fetchall()

    return render_template('pages/profile.html', posts=posts)



