from index_сurator import IndexCurator
from document_curator import DocumentCurator
import sys
import logging

logging.basicConfig(level=logging.INFO)

threshold_time_in_seconds_arg = 'threshold_time_in_seconds'
threshold_size_in_bytes_arg = 'threshold_size_in_bytes'
indices_pattern_list = ['argocd-*','elastic-system-*','monitoring-*','cert-manager-*']

args = {}
if len(sys.argv) > 1:
    for i in range(len(sys.argv)):
        if i != 0:
            item = sys.argv[i]
            key_value_array = item.split('=')
            key = key_value_array[0]
            value = key_value_array[1]
            args[key] = value



indexCurator = IndexCurator()

if threshold_time_in_seconds_arg in args:
    threshold_time_in_seconds = args[threshold_time_in_seconds_arg]
    for indices_pattern in indices_pattern_list:
        indexCurator.delete_indices_by_creation_date(indices_pattern, threshold_time_in_seconds)
else:
    for indices_pattern in indices_pattern_list:
        indexCurator.delete_indices_by_creation_date(indices_pattern)


if threshold_size_in_bytes_arg in args:
    threshold_size_in_bytes = args[threshold_size_in_bytes_arg]
    indexCurator.delete_indeces_by_size(threshold_size_in_bytes)
else:
    indexCurator.delete_indeces_by_size()


# documentCurator = DocumentCurator()
#
# body = {
#   "query": {
#     "term": {
#       "level": {
#         "value": "info"
#       }
#     }
#   }
# }
# documentCurator.delete_document_by_query(body, index_name="*")
