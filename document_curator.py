import os
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta



class DocumentCurator(object):

    def __init__(self):

        try:
            self.CLOUD_ID = os.environ['CLOUD_ID']
        except KeyError as e:
            self.CLOUD_ID = None

        self.ELASTICSEARCH_HOST = os.environ['ELASTICSEARCH_HOST']
        self.ELASTICSEARCH_USER = os.environ['ELASTICSEARCH_USER']
        self.ELASTICSEARCH_PASSWORD = os.environ['ELASTICSEARCH_PASSWORD']
        self.ELASTICSEARCH_PORT = os.environ['ELASTICSEARCH_PORT']
        self.ELASTICSEARCH_SCHEME = os.environ['ELASTICSEARCH_SCHEME']

        if self.CLOUD_ID != None:
            self.es = Elasticsearch( cloud_id=self.CLOUD_ID , basic_auth=(self.ELASTICSEARCH_USER, self.ELASTICSEARCH_PASSWORD) )
        else:
            host = self.ELASTICSEARCH_SCHEME + '://' + self.ELASTICSEARCH_HOST + ':' + self.ELASTICSEARCH_PORT
            self.es = Elasticsearch(hosts=host, basic_auth=(self.ELASTICSEARCH_USER, self.ELASTICSEARCH_PASSWORD), verify_certs=False)

    def delete_document_by_query(self, body, index_name="*" ):
        self.es.delete_by_query(index=index_name, body=body)
