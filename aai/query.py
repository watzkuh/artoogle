import urllib

import rdflib
from rdflib.namespace import RDF, FOAF
import rdflib.plugins.sparql as sparql


class RDFQueries:

    def __init__(self):
        self.g = rdflib.Graph()
        self.g.parse(source='aai/data/data.owl', format="n3")
        self.g.parse(source='aai/data/images.owl', format="n3")
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

    def get_abstract(self, artist):
        urllib.parse.unquote(artist)
        artist = artist.replace(' ', '_')
        q_str = """SELECT * WHERE {
                        <http://dbpedia.org/resource/%s> <http://dbpedia.org/ontology/abstract> ?p .
                    }
                    """
        q = sparql.prepareQuery(q_str % artist)
        res = (self.g.query(q))
        abstract = ""
        for row in res:
            abstract = row[0]
        abstract = abstract.replace('\\xa0', ' ').replace('\\\'s', '\'s')
        return abstract

    def get_art(self, artist):
        urllib.parse.unquote(artist)
        artist = artist.replace(' ', '_')
        print(artist)
        q_str = """
        PREFIX dbp:	<http://dbpedia.org/property/>
        PREFIX local: <http://localhost/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?path ?label WHERE {
            ?a dbp:artist 	<http://dbpedia.org/resource/%s>.
            ?a local:compressed_depiction ?path.
            ?a rdfs:label ?label.
        }
        """
        q = sparql.prepareQuery(q_str % artist)
        res = (self.g.query(q))
        images = {}
        for row in res:
            print(str(row))
            images[row[1]] = row[0]
        return images
