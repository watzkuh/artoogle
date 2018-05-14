import rdflib
from rdflib.namespace import RDF, FOAF


class RDFQueries:

    def __init__(self):
        self.g = rdflib.Graph()
        self.g.parse(source='aai/data/data.owl', format="n3")
        self.g.bind("rdf", RDF)
        self.g.bind("foaf", FOAF)

    def artist_names(self):
        q_result = self.g.query(
            """SELECT * WHERE {
            ?p rdf:type <http://dbpedia.org/ontology/Person> .
            }
            """
        )
        names = []
        for row in q_result:
            names.append(str(row).rsplit('/', 1)[-1].rsplit('\'', 1)[0].replace('_', ' ').lower())
        return names
