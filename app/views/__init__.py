from os.path import join as path_join

from flask import render_template, send_file

from app.views import users
from app import app


@app.route('/')
def index():
    return render_template(
        'home.html',
        title='Bienvenue sur WETA !',
        subtitle='Workshop Enhanced Token Administration'
    )


@app.route('/static/<path:path>')
def get_static(path):
    try:
        return send_file(path_join(app.root_path, "static", path))
    except IOError as e:
        pass
    return "Not Found", 404
