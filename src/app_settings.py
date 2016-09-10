import os
import configparser

class AppSettings:

    def __init__(self):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.config_file = current_dir + "/xpatheva.conf"

        self.debug = 0

        # Current window size
        self.window_height = 300
        self.window_width = 400
        self.read()

        # Current position
        self.x_position = 300
        self.y_position = 300

        # Default window size
        self.default_height = 300
        self.default_width = 400

    def reset(self):
        # Reset settings to defaults
        self.window_height = self.default_height
        self.window_width = self.default_width
        self.debug = 0

    def read(self):
        # Read settings
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_file)
        window_section = config_parser['Window']
        self.window_width = int(window_section['width'])
        self.window_height = int(window_section['height'])
        debugging_section = config_parser['Debugging']
        self.debug = int(debugging_section['debug'])
        pass

    def update(self):
        # Update settings
        pass

    def get_instance(self):
        # Experimental method:
        # use this instead of passing settings as __init__(self, settings)
        pass
