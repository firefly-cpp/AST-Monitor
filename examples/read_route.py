'''Example for reading a route from a file and printing it to the console.'''

from ast_monitor.route_reader import RouteReader

if __name__ == '__main__':
    route_reader = RouteReader('../development/routes/route.json')
    route = route_reader.read()
    polyline = route_reader.get_polyline(route)
    print(route)
