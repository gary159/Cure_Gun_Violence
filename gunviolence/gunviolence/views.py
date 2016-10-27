from gunviolence import app
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template
from werkzeug.serving import run_simple


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)