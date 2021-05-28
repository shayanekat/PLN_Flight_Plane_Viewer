#!/usr/bin/env python

"""
Shayane Kachera
Local package
"""

import matplotlib.pyplot as plt
from numpy import source
# import cartopy.crs as ccrs
import simplekml

#%% function definition part
def parse_pln_file(filename):
    """
    function to convert data in pln file into python object without any other procssing

    Args:
        filename (str): directory to pln file

    Returns:
        dictionnary: python dictionnary contain all data
    """
    with open(filename, 'r') as f:
        # init
        dic = {}
        X, Y = [], []
        
        for l in f.readlines():
            # set title
            if l[9:14] == "Title":
                dic["title"] = l[15:27]
            
            # set coordinates
            if l[13:26] == "WorldPosition":
                # latitude
                raw = l[27:].split(',')
                raw0 = raw[0].split(' ')
                y = float(raw0[0][1:3]) + float(raw0[1][:-1])/60 + float(raw0[-1][:-1])/3600
                if raw[0][0] == 'S':
                    y *= -1
                Y.append(y)
                
                # longitude
                raw1 = raw[1].split(' ')
                x = float(raw1[0][1:-2]) + float(raw1[1][:-1])/60 + float(raw1[-1][:-1])/3600
                if raw[1][0] == 'W':
                    x *= -1
                X.append(x)
            dic['latitudes'] = Y
            dic['longitudes'] = X
        
        return dic



def display(dictionary):
    """
    function to dislay the waypoints on a world map 
    (disclaimer : this method is better for IFR liner flight plans because it is not precise)

    Args:
        source_dictionary (dictionnary): the dictionnary with the first process
    """
    # initialize display
    im = plt.imread("background.png")
    implot = plt.imshow(im)
    
    # process data for plotting
    X, Y = [], []
    for i in range(len(dictionary['latitudes'])):
        X.append(dictionary['longitudes'][i] + 180)
        Y.append(dictionary['latitudes'][i]*(-1) + 90)
    
    # plot data
    plt.plot(X, Y, label='Route')
    plt.scatter(X, Y, label="waypoints")
    plt.scatter(X[0], Y[0], label="starting point")
    plt.scatter(X[-1], Y[-1], label="destination point")
    
    plt.title(dictionary["title"])
    plt.xlabel("longitude (°)")
    plt.ylabel("latitude (°)")
    plt.legend()
    
    plt.show()

def save_kml_file(source_dictionnary, filename):
    """
    function to save data into kml file that is openable with google earth

    Args:
        source_dictionnary (dictionnary): data to convert
        filename (string) the name of the file that will be created
    """
    # convert & save data
    kml = simplekml.Kml()
    for i in range(len(source_dictionnary["latitudes"])):
        kml.newpoint(name=str(i), coords=[(source_dictionnary["longitudes"][i], source_dictionnary["latitudes"][i])])
    
    kml.save(filename + '.kml')

#%% test part
if __name__ == '__main__':
    dic = parse_pln_file('example.pln')
    save_kml_file(dic, "test")