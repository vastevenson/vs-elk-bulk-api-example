from elasticsearch import Elasticsearch

'''
Usage: es = Create_Elk_Obj().get_elk_obj()
Author: Vincent Stevenson
'''

class Create_Elk_Obj:
    def __init__(self,
                 hosts="localhost:9200"):
        self.es = Elasticsearch(hosts)

    def get_elk_obj(self):
        return self.es