import rdflib
from rdflib.namespace import RDF, FOAF

g = rdflib.Graph()
g.parse(source='images.owl', format="n3")
g.parse(source='data.owl', format="n3")
g.bind("rdf", RDF)

q = """
    PREFIX local: <http://localhost/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX yago: <http://dbpedia.org/class/yago/>
    PREFIX dbpprop: <http://dbpedia.org/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?artist_name ?artwork_name ?path WHERE {{
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
    LIMIT {1}
    """
q = q.format("Mona Lisa", 3)
res = g.query(q)


for row in res:
    print(row)
