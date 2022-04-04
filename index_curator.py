import os
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import logging


log = logging.getLogger(__name__)


class IndexCurator(object):


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


    def __str__(self):
        return 'CLOUD_ID: ' + str(self.CLOUD_ID) + 'ELASTICSEARCH_HOST: ' + \
                self.ELASTICSEARCH_HOST + 'ELASTICSEARCH_USER: ' + \
                self.ELASTICSEARCH_USER + 'ELASTICSEARCH_PASSWORD: ' + \
                self.ELASTICSEARCH_PASSWORD


    def get_indeces_by_pattern(self, pattern: str):
        return self.es.indices.get(index=pattern)


    """Decorator, commit deleting"""
    def delete_indeces_decorator(get_indeces_for_deleting):
        def delete_indeces(self, *args, **kwargs):
            indeces_for_deleting = get_indeces_for_deleting(self, *args, **kwargs)
            if len(indeces_for_deleting) > 0:
                 indices_deleting_str_list = ','.join(indeces_for_deleting)
                 self.es.indices.delete(index=indices_deleting_str_list)
                 log.info(indices_deleting_str_list + ': have been deleted')
        return delete_indeces

    def is_time_passed(self,threshold_time_in_seconds , compared_time):
        now_in_seconds = datetime.now().timestamp()
        if (now_in_seconds - compared_time) >= threshold_time_in_seconds:
            return True
        else:
            return False


    """default 3 days"""
    @delete_indeces_decorator
    def delete_indices_by_creation_date(self, pattern, threshold_time_in_seconds = 259200):
        indices_for_deleting = []
        indices = self.get_indeces_by_pattern(pattern)
        for key in indices:
            index_creation_time_in_seconds = int(indices[key]['settings']['index']['creation_date']) / 1000
            if self.is_time_passed(threshold_time_in_seconds, index_creation_time_in_seconds):
                indices_for_deleting.append(key)
        return indices_for_deleting


    """default 1GiB"""
    @delete_indeces_decorator
    def delete_indeces_by_size(self, threshold_size_in_bytes = 1073741824):
        indices_for_deleting = []
        cluster_stats = self.es.indices.stats()
        indeces_stats = cluster_stats['indices']
        for key in indeces_stats:
            index_size = int(indeces_stats[key]['total']['store']['size_in_bytes'])
            if index_size >= threshold_size_in_bytes:
                indeces_for_deleting.append(key)
        return indices_for_deleting
