import os
import os.path

from whoosh import index
from whoosh.fields import TEXT, Schema
from whoosh.qparser import QueryParser
from whoosh.reading import TermNotFound

import aai.query as query

SCHEMA = Schema(content=TEXT(phrase=True, stored=True))
INDEX_DIR = 'aai/indices'


def get_indices():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
    if index.exists_in(INDEX_DIR):
        return index.open_dir(INDEX_DIR)
    else:
        return full_index()


def full_index():
    idx = index.create_in(INDEX_DIR, SCHEMA)
    writer = idx.writer()

    data = query.RDFQueries().artist_names()
    for item in data:
        writer.add_document(content=item)

    writer.commit()
    return idx


def search(user_query):
    # get index to search
    idx = get_indices()

    # parse the user_query
    qp = QueryParser('content', schema=idx.schema)
    query = qp.parse(user_query)

    # get searcher
    with idx.searcher() as searcher:
        # do search
        try:
            results = searcher.search(query, limit=7)
        except TermNotFound:
            results = []
        json_A = []
        for hit in results:
            json_A.append(hit['content'])
        return json_A