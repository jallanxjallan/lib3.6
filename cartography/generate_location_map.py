#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_map.py
#  
#  Copyright 2018 Jeremy Allan <jeremy@Jeremyallan.com>
# 

import sys 
import os
import pandas as pd
import os
import csv
from geopy import geocoders
from geopy.geocoders import GoogleV3
import geopandas as gpd
from matplotlib import rc
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from adjustText import adjust_text


base_dir = '/home/jeremy/map_data/natural_earth/'
base_dataset = 'ne_10m_admin_0_countries.shp'
coordinates_file = 'coordinates.csv'
boundaries_file = 'boundaries.csv'
map_file_dir = '/home/jeremy/Desktop/one_man_air_force_maps' 


format_map_base = dict(
    color='0.75', 
    edgecolor='black', 
    linewidth=.25
)

format_marker = dict(
        color='black', 
        marker='.', 
        linewidth=.75, 
        markersize=5
    )
    
format_label = dict(
                    #~ arrowprops=dict(arrowstyle="->", color='r', lw=0.5),
                    autoalign=True, 
                    only_move={'points':'y', 'text':'y'},
                    ha='center',
                    va='top'
                )
    

def export_map(name, fig):
    plt.axis('off')
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['lines.markersize'] = 2
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.size'] = 8

    fig.figsize = (8.22, 5.5) 
    #~ plt.show()
   
    plt.savefig(os.path.join(map_file_dir, name + '.svg'), transparent=True)

def plot_base(ax, base, places, bounds):
    for country in places.country.unique():
        b = base[base.SOVEREIGNT == country] 
        b.plot(ax=ax, **format_map_base) 
    plt.xlim(bounds.minlng, bounds.maxlng)
    plt.ylim(bounds.minlat, bounds.maxlat)


def set_labels(places):
    # Now we plot the texts for each scatter point using the "Label" column defined earlier
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.size'] = 8
    texts = []
    for x, y, label in zip(places.geometry.x, places.geometry.y, places["name"]):
        texts.append(plt.text(x, y, label))

    # And NOW we adjust those points so that they no longer overlap
    adjust_text(texts, **format_label)



def set_annotation(ax, row):
    print(row)
    xoff = row['xoff'] 
    yoff = row['yoff'] 
    label = row['label']    
    ax.annotate(
                s=label, 
                xy=row.geometry.coords[0], 
                xytext=(xoff, yoff), 
                textcoords="offset points",
                arrowprops=dict(arrowstyle="-"),
                fontsize=8,
                ha='right',
                va='bottom'
            )
    

def set_geometry(row, coordinates):
    try:
        crow = coordinates.loc[coordinates['name'] == row['name']]
    except:
        raise
    if crow.empty:
        return None
    return Point(crow['lng'], crow['lat'])
    
def set_places(map_name, coordinates):
    pd_set =  pd.read_csv(map_name + '.csv')
    print(pd_set)
    pd_set['country'] = pd_set['name'].map(coordinates.set_index('name')['country'])
    places = gpd.GeoDataFrame(pd_set)
    places['geometry'] = places.apply(lambda row: set_geometry(row, coordinates), axis=1)
    return places


def generate_map(map_name):
    base = gpd.read_file(os.path.join(base_dir, base_dataset))
    coordinates = pd.read_csv(coordinates_file)
    places = set_places(map_name, coordinates)
    bounds = pd.read_csv(boundaries_file)
    fig, ax  = plt.subplots()
    plot_base(ax, base, places, next((b for b in bounds.itertuples() if b.name == map_name), None))
    places.plot(ax=ax, **format_marker)
    #~ places.apply(lambda row: set_annotation(ax, row), axis=1)
    set_labels(places)
    export_map(map_name, fig)
    
if __name__ == '__main__':
    generate_map(sys.argv[1])
