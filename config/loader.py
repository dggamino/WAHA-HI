"""
Configuration loader.
"""


import os

from config.defaults import DEFAULT_CONFIG



class ConfigLoader:


    def load(self):

        config = DEFAULT_CONFIG.copy()


        for key in config:

            if key in os.environ:

                config[key] = os.environ[key]


        return config
