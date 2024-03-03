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
    return render_template('pages/index.html')#, posts=posts)

@bp.route('/home', methods =['GET', 'POST'])
def home():
    return render_template('pages/home.html')#, posts=posts)

@bp.route('/profile', methods =['GET', 'POST'])
def profile():
    cards = []

    for card_number in range(1, 7):  # Adjust the range as needed
        card = {
            'title': f'Name: {card_number}',
            'events': [
                {'name': f'Event {i}', 'description': f'Description for Event {i}'}
                for i in range(1, 4)  # Adjust the range as needed
            ]
        }
        cards.append(card)

    return render_template('pages/profile.html', cards=cards)

@bp.route('/register_child', methods =['GET', 'POST'])
def register_child():
    return render_template('pages/register_child.html')#, posts=posts)