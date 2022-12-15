__author__ = 'XXX'


from coolest.io.analysis import Analysis


class Plotting(object):
    """
    Handles computation of model-independent quantities and other analysis computations
    """

    def __init__(self, coolest_file_path):
        self.analysis = Analysis(coolest_file_path)
        self.coolest_data = self.analysis.coolest_data

    def plot_summary(self):
        pass
