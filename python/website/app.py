from flask import abort, g, render_template

from database.schema import Citizen, citizen_database
from website import app
from website.image import render_image


@app.before_request
def load_user():
    g.user = {'name': 'me'}


@app.route('/')
def index():
    with citizen_database:
        citizens = citizen_database.session.query(Citizen).limit(100).all()
        citizen_database.session.commit()
        map_name = render_image(citizens)
        return render_template(
            'index.html',
            citizens=citizens,
            map_name=map_name,
        )


@app.route('/citizen/<citizen_id>')
def get_citizen(citizen_id):
    with citizen_database:
        citizen = (
            citizen_database.session.query(Citizen)
            .filter(Citizen.citizen_id == citizen_id)
            .one_or_none()
        )
        if not citizen:
            abort(404)

        map_name = render_image([citizen])
        return render_template(
            'citizen.html',
            citizen=citizen,
            map_name=map_name,
        )


@app.route('/search')
def search():
    return render_template('search.html')
