"""
From https://github.com/hankhank10/msfs-pln-file-parser/blob/main/parse_pln.py
credit to hankhank10, modified my myself
"""

import xmltodict
import matplotlib.pyplot as plt
import json
import cartopy.crs as ccrs
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
    with open(filename, 'r') as xmlfile:
        xml_string = xmlfile.read()

    xml_string = xml_string.replace('°', '')

    output_dictionary = xmltodict.parse(xml_string)
    return output_dictionary


def fix_waypoints(source_dictionary):
    """
    function to process waypoints coordinates and convert into decimal coordinates

    Args:
        source_dictionary (dictionnary): the original dicitionnary

    Returns:
        dictonnary: dictionnary with the first process done
    """
    for waypoint in source_dictionary['SimBase.Document']['FlightPlan.FlightPlan']['ATCWaypoint']:

        # Split into constituent parts
        waypoint['Latitude'] = waypoint['WorldPosition'].split(",")[0]
        waypoint['Longitude'] = waypoint['WorldPosition'].split(",")[1]
        waypoint['Altitude'] = waypoint['WorldPosition'].split(",")[2]

        # Tidy altitude
        waypoint['Altitude'] = float(waypoint['Altitude'])

        # Work out latitude
        latitude_direction = waypoint['Latitude'][0]
        rest_of_latitude = waypoint['Latitude'][1:]

        latitude_degrees = rest_of_latitude.split(" ")[0]
        latitude_minutes = rest_of_latitude.split(" ")[1]
        latitude_seconds = rest_of_latitude.split(" ")[2]

        latitude_minutes = latitude_minutes.split("'")[0]
        latitude_seconds = latitude_seconds.split('"')[0]

        latitude_degrees = int(latitude_degrees.replace('Â', ''))
        latitude_minutes = int(latitude_minutes)
        latitude_seconds = float(latitude_seconds)

        latitude_decimal = latitude_degrees + (latitude_minutes / 60) + (latitude_seconds / 3600)
        # print(str(latitude_degrees), str(latitude_minutes), str(latitude_seconds), ">", str(latitude_decimal))

        if latitude_direction == "S":
            latitude_decimal = -latitude_decimal
        waypoint['DecimalLatitude'] = latitude_decimal

        # Work out longitude
        longitude_direction = waypoint['Longitude'][0]
        rest_of_longitude = waypoint['Longitude'][1:]

        longitude_degrees = rest_of_longitude.split(" ")[0]
        longitude_minutes = rest_of_longitude.split(" ")[1]
        longitude_seconds = rest_of_longitude.split(" ")[2]

        longitude_minutes = longitude_minutes.split("'")[0]
        longitude_seconds = longitude_seconds.split('"')[0]

        longitude_degrees = int(longitude_degrees.replace('Â', ''))
        longitude_minutes = int(longitude_minutes)
        longitude_seconds = float(longitude_seconds)

        longitude_decimal = longitude_degrees + (longitude_minutes / 60) + (longitude_seconds / 3600)
        #print(str(longitude_degrees), str(longitude_minutes), str(longitude_seconds), ">", str(longitude_decimal))

        if longitude_direction == "W":
            longitude_decimal = -longitude_decimal
        waypoint['DecimalLongitude'] = longitude_decimal

    return source_dictionary


def simplify_route(source_dictionary):
    """
    function to simplify the dictionnary by removing all unecessary data

    Args:
        source_dictionary (dictionnary): the data with first process

    Returns:
        dictionnary: output dictionnary that is simplified
    """
    output_dictionary = []

    a = 0
    for waypoint in source_dictionary['SimBase.Document']['FlightPlan.FlightPlan']['ATCWaypoint']:
        this_waypoint = {
            'id': a,
            'latitude': waypoint['DecimalLatitude'],
            'longitude': waypoint['DecimalLongitude']
        }
        output_dictionary.append(this_waypoint)
        a = a + 1

    output_dictionary = {
        'status': 'success',
        'waypoints': output_dictionary
    }

    return output_dictionary


def save_json_file(output_filename, source_dictionary):
    """
    function to save the data as a json file

    Args:
        output_filename (string): the name of the json file that will be created
        source_dictionary (dictionnary): the data you want to convert into json file
    """
    with open(output_filename, 'w') as jsonfile:
        json.dump(source_dictionary['SimBase.Document']['FlightPlan.FlightPlan'], jsonfile, indent=4)


def display(source_dictionary):
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
    dictionnary = simplify_route(source_dictionary)
    X, Y = [], []
    for wp in dictionnary['waypoints']:
        X.append(wp['longitude'] + 180)
        Y.append(-wp['latitude'] + 90)
    
    # plot data
    plt.plot(X, Y, label='Route')
    plt.scatter(X, Y, label="waypoints")
    plt.scatter(X[0], Y[0], label="starting point")
    plt.scatter(X[-1], Y[-1], label="destination point")
    
    plt.title(source_dictionary['SimBase.Document']['FlightPlan.FlightPlan']["Title"])
    plt.xlabel("longitude (°)")
    plt.ylabel("latitude (°)")
    plt.legend()
    
    plt.show()

def mapview(source_dictionary):
    """
    function to get a better display than with the other function

    Args:
        source_dictionary (dictionnary): the dictionnary with first process
    """
    margin = 5
    # initialize display
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()

    # process data for plotting
    dictionnary = simplify_route(source_dictionary)
    X, Y = [], []
    for wp in dictionnary['waypoints']:
        X.append(wp['longitude'])
        Y.append(wp['latitude'])
    
    ax.set_extent([min(X)-margin, max(X)+margin, min(Y)-margin/2, max(Y)+margin/2], ccrs.PlateCarree())
    
    # plot data
    plt.plot(X, Y, label='Route')
    plt.scatter(X, Y, label="waypoints")
    plt.scatter(X[0], Y[0], label="starting point")
    plt.scatter(X[-1], Y[-1], label="destination point")
    
    plt.title(source_dictionary['SimBase.Document']['FlightPlan.FlightPlan']["Title"])
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
    # filename = "kml_data"
    
    kml = simplekml.Kml()
    for wp in source_dictionnary['waypoints']:
        kml.newpoint(name=str(wp['id']), coords=[(wp['longitude'], wp['latitude'])])
    
    kml.save(filename + '.kml')

#%% test part
if __name__ == '__main__':
    data = parse_pln_file('example.pln') # parse data
    data = fix_waypoints(data) # first process
    data_processed = simplify_route(data) # second process
    save_kml_file(data_processed) # generate kml file
    # pln_parser.mapview(data) # view data