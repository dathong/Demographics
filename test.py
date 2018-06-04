from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), content=TEXT)
import os
import pandas as pd

index_dir = "indexdir"
os.system("rm -r " + index_dir + "/*")


if not os.path.exists(index_dir):
    os.mkdir(index_dir)

ix = create_in(index_dir, schema)
writer = ix.writer()
writer.add_document(title=u"First document", content="I love my life")
writer.add_document(title=u"Second document", content="I love my damn life")
writer.add_document(title=u"3 document", content="I love my damn fucking life")
writer.add_document(title=u"4 document", content="I love my damn fucking awesome life")
writer.commit()
from whoosh.qparser import QueryParser

q = "life"
with ix.searcher() as searcher:

        print("q = ",q)
        q = '"love life"~2'
        print("q = ",q)
        query = QueryParser("content", ix.schema).parse(q)
        results = searcher.search(query)
        for rs in results:
            print(rs['title'],rs['content'])