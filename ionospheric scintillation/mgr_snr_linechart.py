class Satellite:
    def __init__(self, name):
        self.name = name
        self.data = []


def create_satellite_list():
    pass


def parse_query_to_satellite(queryresults):
    pass


def create_snr_chart():
    pass


def wrapper(queryresults):
    sat_list = create_satellite_list()
    parse_query_to_satellite(queryresults)
    create_snr_chart()
