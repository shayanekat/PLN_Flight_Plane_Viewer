import pln_parser

data = pln_parser.parse_pln_file('example.pln') # parse data
data = pln_parser.fix_waypoints(data) # first process
data_processed = pln_parser.simplify_route(data) # second process
pln_parser.save_kml_file(data_processed) # generate kml file
# pln_parser.mapview(data) # view data
