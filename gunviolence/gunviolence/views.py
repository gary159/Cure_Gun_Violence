from gunviolence import app
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template, url_for
from werkzeug.serving import run_simple
from ConfigUtil import config
from ChicagoData import comm
import pandas as pd
import numpy as np
import random

def gen_hex_colour_code():
   return ''.join([random.choice('0123456789ABCDEF') for x in range(6)])


key=config['GOOGLE_MAPS_KEY']
GoogleMaps(app, key=key)




@app.route('/')
def main_page():
	return render_template('main_page.html')



@app.route('/chicago')
def chicago():
    city_map = Map(
        identifier="view-side",
        zoom=11,
        center=(41.8781136, -87.6298),        
        maptype='ROADMAP',
        zoom_control=True,
        scroll_wheel=False,
        fullscreen_control=False,
        rorate_control=False,
        maptype_control=False,
        streetview_control=False,
        style="height:800px;width:600px;margin:0;"
    )
    
    return render_template('map.html', city_map=city_map, date_dropdown=[d for d in enumerate(comm.date_list)], data=comm.data)



@app.route('/chicago/<string:dt_filter>')
def chicago_dt(dt_filter):
    city_map = Map(
        identifier="view-side",
        zoom=11,
        center=(41.8781136, -87.6298),        
        maptype='ROADMAP',
        zoom_control=True,
        scroll_wheel=False,
        fullscreen_control=False,
        rorate_control=False,
        maptype_control=False,
        streetview_control=False,
        style="height:800px;width:600px;margin:0;"
    )
    polyargs = {}
    cols = set(comm.data.columns) - set(comm.date_list) 
    cols |= set([dt_filter])
    comm_data = comm.geom_to_list(comm.data[list(cols)])
    comm_data['norm'] = np.linalg.norm(comm_data[dt_filter])

    for index, row in comm_data.iterrows():
        # col = gen_hex_colour_code()
        polyargs['stroke_color'] = '#FF0000' #'#%s' % col
        polyargs['fill_color'] = '#FF0000' #'#%s' % col
        path = [p for p in row['the_geom_community']]
        polyargs['stroke_opacity'] = .8
        polyargs['stroke_weight'] = 1
        polyargs['fill_opacity'] = row[dt_filter]/row['norm']
        city_map.add_polygon(path=path, **polyargs)
    return render_template('map.html', city_map=city_map, date_dropdown=[d for d in enumerate(comm.date_list)], data=comm.data)


if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)