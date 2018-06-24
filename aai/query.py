import rdflib
import rdflib.plugins.sparql as sparql
from rdflib.namespace import RDF, FOAF
import random


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

    def get_art_from_artist(self, artist):
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
            images[row[0]] = row[1]
        return images

    def get_artist_from_art(self, artwork):
        artwork = artwork.replace(' ', '_')
        q_str = """
                PREFIX dbp:	<http://dbpedia.org/property/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?label WHERE {
                    <http://dbpedia.org/resource/%s> dbp:artist ?a.
                    ?a rdfs:label ?label.
                }
                """
        q = sparql.prepareQuery(q_str % artwork)
        res = (self.g.query(q))
        artist = ""
        for row in res:
            artist = str(row[0])
        return artist

    def get_artists_for_movement(self, movement):
        if not movement:
            return

        string = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX db: <http://dbpedia.org/resource/>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                SELECT ?l WHERE {{
                    ?a dbo:movement/rdfs:label "%s"@en.
                    ?a rdfs:label ?l
                }}
        """
        q = sparql.prepareQuery(string % movement)
        res = self.g.query(q)
        artists = []
        for row in res:
            artists.append(str(row.l))
        return artists

    def get_movement(self, artist):
        q_str = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                SELECT * WHERE {
                    <http://dbpedia.org/resource/%s> dbo:movement/rdfs:label ?m  
                }
                """
        q = sparql.prepareQuery(q_str % artist)
        res = (self.g.query(q))
        for row in res:
            return row.m

    def get_birthplace(self, artist):
        q_str = """
                       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                       PREFIX dbo: <http://dbpedia.org/ontology/>
                       SELECT * WHERE {
                           <http://dbpedia.org/resource/%s> dbo:birthPlace ?p
                       }
                       """
        q = sparql.prepareQuery(q_str % artist)
        res = (self.g.query(q))
        for row in res:
            return row.p

    def get_birthdate(self, artist):
        q_str = """
                       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                       PREFIX dbo: <http://dbpedia.org/ontology/>
                       SELECT * WHERE {
                           <http://dbpedia.org/resource/%s> dbo:birthDate ?d
                       }
                       """
        q = sparql.prepareQuery(q_str % artist)
        res = (self.g.query(q))
        for row in res:
            return row.d

    def get_similar_art(self, artwork, count=10):
        q = """
            PREFIX local: <http://localhost/>
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX dbpprop: <http://dbpedia.org/property/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT distinct ?artist_name ?artwork_name ?path WHERE {{
            ?this_artwork rdfs:label "{0}"@en;
            local:tag ?tag.
            ?similar_artwork local:tag ?tag;
            local:compressed_depiction ?path;
            rdfs:label ?artwork_name;
            rdf:type ?type;
            dbpprop:artist ?artist.
            ?artist rdfs:label ?artist_name.
            FILTER (?similar_artwork != ?this_artwork).
            FILTER (?type = yago:Painting103876519 || ?type = yago:Sculpture104157320).
            }}
            """
        q = q.format(artwork)
        # this may mess up the randomness
        # q = sparql.prepareQuery(q)
        res = self.g.query(q)
        result = []
        res = random.sample(list(res), count)
        for row in res:
            result_row = {"artist": row["artist_name"], "artwork": row["artwork_name"], "path": row["path"]}
            result.append(result_row)
        return result

    def get_artwork_labels(self, artwork):
        q = """
            PREFIX local: <http://localhost/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?tag WHERE {{
                ?this_artwork rdfs:label "{0}"@en;
                local:tag ?tag.
            }}
            """
        q = q.format(artwork)
        q = sparql.prepareQuery(q)
        res = self.g.query(q)
        result = []
        for row in res:
            result.append(row["tag"])
        return result
