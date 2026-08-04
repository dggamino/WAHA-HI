"""
Runtime configuration object.
"""


from config.loader import ConfigLoader



class RuntimeConfig:


    def __init__(self):

        loader = ConfigLoader()

        self.values = loader.load()



    def get(
        self,
        key,
        default=None
    ):

        return self.values.get(
            key,
            default
        )



    def all(self):

        return self.values
