import math


class GoalsProcessor:
    def __init__(self, route):
        """Class for measuring the progress of the user on the route."""
        self.position = None
        self.total_ascent = route["evaluation"]["total_ascent"]
        self.total_distance = route["evaluation"]["total_distance"]
        self.ascents = route["ascents"]
        self.distances = route["distances"]
        self.current_distance = 0
        self.current_ascent = 0
        self.progress = 0
        self.distance_to_go = sum(self.distances)
        self.ascent_to_go = sum(self.ascents)
        self.index_closest = None
        self.route = route
        filteredIntersections = [sublist[1] for sublist in route["nodes"]]

        # Filter the list of dictionaries based on the IDs and remove duplicates
        filtered_list = []
        last_added_id = None

        for obj in route['route_render']:
            # Check if the id is in filteredIntersections
            if obj['id'] in filteredIntersections:
                # Check if the id is the same as the last added id
                if obj['id'] != last_added_id:
                    # Add the object to the filtered list
                    filtered_list.append(obj)

                    # Update the last added id
                    last_added_id = obj['id']

        # Now filtered_list contains the filtered and unique dictionaries
        self.filtered_list = filtered_list
        a = 100

    def add_position(self, position):
        """Add the current position of the user."""
        self.position = position[0:2]
        self.get_progress(self.position)

    def get_progress(self, position):
        """Calculate the progress of the user on the route, (%) of route, Ascent, Distance."""
        current_node = self.find_closest_object(position)
        distance = self.haversine_distance(position, (current_node['lat'], current_node['lon']))
        if distance < 0.05:
            self.current_distance += sum(self.distances[0:self.index_closest + 1])
            self.current_ascent += sum(self.ascents[0:self.index_closest + 1])
            # remove the summed indexes
            self.distances = self.distances[self.index_closest + 1:]
            self.ascents = self.ascents[self.index_closest + 1:]
            self.filtered_list = self.filtered_list[self.index_closest + 1:]
            self.index_closest = None
            self.distance_to_go = self.total_distance - self.current_distance
            self.ascent_to_go = self.total_ascent - self.current_ascent
            self.progress = self.current_distance / self.total_distance

    def find_closest_object(self, position):
        """Finds the closest object in the list to the given point."""
        smallest_diff = float('inf')
        closest_object = None

        index = 0
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
                self.index_closest = index
            index += 1

        return closest_object  # Return the closest object

    def haversine_distance(self, coord1, coord2):
        """
        Calculate the Haversine distance between two points on the Earth specified by latitude/longitude.
        """

        # Radius of Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

        # Compute differences in latitude and longitude
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c

        return distance
