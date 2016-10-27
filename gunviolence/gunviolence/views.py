from gunviolence import app
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template, url_for
from werkzeug.serving import run_simple
from ConfigUtil import config

key=config['GOOGLE_MAPS_KEY']
GoogleMaps(app, key=key)

@app.route('/')
def main_page():
	return render_template('main_page.html')

@app.route('/chicago')
def chicago():
    # creating a map in the view
    city_map = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        maptype='ROADMAP',
        zoom_control=True,
        markers=[(37.4419, -122.1419)]
    )
    
    return render_template('map.html', city_map=city_map)



if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)