from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
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
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('pages/index.html')#, posts=posts)

@bp.route('/home', methods =['GET', 'POST'])
def home():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('pages/home.html')#, posts=posts)