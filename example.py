import pln_parser

data = pln_parser.parse_pln_file('example.pln')
data = pln_parser.fix_waypoints(data)
data_processed = pln_parser.simplify_route(data)
pln_parser.mapview(data)
