from flask import g, render_template

from website import app
from database.schema import Citizen, citizen_database


@app.before_request
def load_user():
    g.user = {'name': 'me'}


@app.route('/', methods=['GET', 'POST'])
def index():
    with citizen_database:
        citizens = citizen_database.session.query(Citizen).limit(50)
    return render_template('index.html', citizens=citizens)


@app.route('/search')
def search():
    return render_template('search.html')
