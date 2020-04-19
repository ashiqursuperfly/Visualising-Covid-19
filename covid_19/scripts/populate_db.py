from main_app.api.api import *
from main_app.views import GraphFile
# from ..main_app.api.api import ApiInfo

def run():
    populate_db(GraphFile.LIMIT_COUNTRIES, GraphFile.SHOULD_FETCH_COUNTRIES)
    print("Done")
