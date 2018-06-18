import os
import os.path

from whoosh import index, analysis, searching
from whoosh.fields import TEXT, Schema
from whoosh.qparser import QueryParser
from whoosh.reading import TermNotFound

import aai.query as query

SCHEMA = Schema(content=TEXT(stored=True, spelling=True))
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


def search(query_string):
    limit = 7
    # get index to search
    idx = get_indices()

    # parse the user_query
    qp = QueryParser('content', schema=idx.schema)
    query = qp.parse(query_string + '*')

    # get searcher
    with idx.searcher() as searcher:
        # first step: try pure autocomplete
        try:
            results = searcher.search(query, limit=limit)
        except TermNotFound:
            results = []
        json_A = []
        for hit in results:
            json_A.append(hit['content'])
        # augment with spell checking suggestions
        if len(json_A) == 0:
            corrector = searcher.corrector('content')
            results = corrector.suggest(query_string, limit=5)
            for hit in results:
                try:
                    query = qp.parse(hit + '*')
                    limit = limit - len(json_A)
                    if limit >= 1:
                        res = searcher.search(query, limit=limit)
                    else:
                        res = searcher.search(query, limit=5)
                except TermNotFound:
                    res = []
                for h in res:
                    json_A.append(h['content'])
        return json_A
