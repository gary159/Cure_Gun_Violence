from gunviolence import app
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template, url_for
from werkzeug.serving import run_simple
from ConfigUtil import config
from data import ChicagoData

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
        zoom=12,
        center=(41.8781136, -87.6298),        
        maptype='ROADMAP',
        zoom_control=True,
        scroll_wheel=False,
        fullscreen_control=False,
        rorate_control=False,
        maptype_control=False,
        streetview_control=False,
        style="height:700px;width:500px;margin:0;"
    )

    return render_template('map.html', city_map=city_map)



if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)