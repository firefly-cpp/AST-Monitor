import http.server
import os
from urllib.parse import urlparse


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve the html files from the dist folder instead of the root folder.
    The handler helps us avoid changing the current directory of the Python script."""

    def translate_path(self, path):
        """
        Method that allows the server to serve the html files from the dist folder instead of the root folder.
        Args:
            path: url path

        Returns:

        """
        parsed_path = urlparse(path).path
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        custom_folder = os.path.join(current_file_directory, 'map', 'dist')
        translated_path = os.path.join(custom_folder, parsed_path.lstrip('/'))
        print(f"Translated path: {translated_path}")  # Debugging line to print the translated path
        return translated_path
