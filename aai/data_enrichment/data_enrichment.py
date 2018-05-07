import rdflib
import requests
from rdflib.namespace import FOAF
from google_images_download import google_images_download

graph = rdflib.Graph()
graph.parse('data.owl', format="n3")

result = graph.query("""
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX yago: <http://dbpedia.org/class/yago/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpprop: <http://dbpedia.org/property/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?name ?depiction WHERE { ?entity foaf:depiction ?depiction. ?entity rdfs:label ?name}
    """)

i = 0
count = len(result)
print(count)
for s in result:
    try:
        print(round((i / count) * 100, 2), " %")
        i = i + 1
        print("Accessing...", str(s.depiction))
        if requests.get(s.depiction).status_code != 200:
            print("Fallback: Searching Google for " + s.name)
            response = google_images_download.googleimagesdownload()
            arguments = {"keywords": "'" + s.name +
                                     "'", "limit": 1, "prefix": s.name}
            response.download(arguments)
    except:
        continue
