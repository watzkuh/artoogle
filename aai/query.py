import rdflib
import requests
from rdflib.namespace import FOAF
from google_images_download import google_images_download

class ArtQuery:

    def __init__(self, file):
        self.x = x
        self.y = y
        self.description = "This shape has not been described yet"
        self.author = "Nobody has claimed to make this shape yet"


graph = rdflib.Graph()
graph.parse('data.owl', format="n3")

graph.load()
