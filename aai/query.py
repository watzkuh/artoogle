import rdflib
from rdflib.namespace import RDF, FOAF
import rdflib.plugins.sparql as sparql

class RDFQueries:

    def __init__(self):
        self.g = rdflib.Graph()
        self.g.parse(source='aai/data/data.owl', format="n3")
        self.g.bind("rdf", RDF)
        self.g.bind("foaf", FOAF)

    def artist_names(self):
        res = self.g.query(
            """SELECT * WHERE {
                ?p rdf:type <http://dbpedia.org/ontology/Person> .
            }
            """
        )
        names = []
        for row in res:
            names.append(str(row).rsplit('/', 1)[-1].rsplit('\'', 1)[0].replace('_', ' '))
        return names

    def get_artist(self, name):
        name = name.replace(' ', '_')
        q_str = """SELECT * WHERE {
                <http://dbpedia.org/resource/%s> <http://dbpedia.org/ontology/abstract> ?p .
            }
            """
        q = sparql.prepareQuery(q_str % name)
        res = str(self.g.query(q))
        
        return res
