import math


class GoalsProcessor:
    def __init__(self, route):
        self.positions = []
        self.route = route
        filteredIntersections = [sublist[1] for sublist in route["nodes"]]
        # Set to keep track of unique IDs
        unique_ids = set()

        # Filter the list of dictionaries based on the IDs and remove duplicates
        filtered_list = []
        for obj in self.route['route_render']:
            if obj['id'] in filteredIntersections and obj['id'] not in unique_ids:
                filtered_list.append(obj)
                unique_ids.add(obj['id'])

        # Now filtered_list contains the filtered and unique dictionaries
        self.filtered_list = filtered_list

        a = 100

    def add_position(self, position):
        if len(self.positions) >= 20:
            self.positions.pop(0)  # Remove the first element
        self.positions.append([position[0], position[1]])  # Add the new element to the end

    def find_closest_object(self, position):
        smallest_diff = float('inf')
        closest_object = None

        # Loop through each object in the list
        for obj in self.filtered_list:
            lat_diff = math.fabs(obj['lat'] - position[0])
            lon_diff = math.fabs(obj['lon'] - position[1])

            # Calculate the total difference for both latitude and longitude
            total_diff = lat_diff + lon_diff

            # Update smallest_diff and closest_object if this object is closer to the given point
            if total_diff < smallest_diff:
                smallest_diff = total_diff
                closest_object = obj
