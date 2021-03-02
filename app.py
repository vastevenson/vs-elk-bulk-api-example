from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import json
from elk_obj_create import Create_Elk_Obj
# declare a client instance of the Python Elasticsearch library
client = Create_Elk_Obj().get_elk_obj()

# adapted from: https://kb.objectrocket.com/elasticsearch/how-to-bulk-index-elasticsearch-documents-from-a-json-file-using-python-753

# define a function that will load a text file
def get_data_from_text_file(self):
    # the function will return a list of docs
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]

# call the function to get the string data containing docs
docs = get_data_from_text_file("data.json")

# print the length of the documents in the string
print ("String docs length:", len(docs))

# define an empty list for the Elasticsearch docs
doc_list = []

# use Python's enumerate() function to iterate over list of doc strings
for num, doc in enumerate(docs):
    # catch any JSON loads() errors
    try:
        # prevent JSONDecodeError resulting from Python uppercase boolean
        doc = doc.replace("True", "true")
        doc = doc.replace("False", "false")
        # convert the string to a dict object
        dict_doc = json.loads(doc)
        # add a new field to the Elasticsearch doc
        dict_doc["timestamp"] = datetime.now()
        # add a dict key called "_id" if you'd like to specify an ID for the doc
        dict_doc["_id"] = num
        # append the dict object to the list []
        doc_list += [dict_doc]

    except json.decoder.JSONDecodeError as err:
        # print the errors
        print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)
print ("Dict docs length:", len(doc_list))

# attempt to index the dictionary entries using the helpers.bulk() method
try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")

    # use the helpers library's Bulk API to index list of Elasticsearch docs
    resp = helpers.bulk(
    client,
    doc_list,
    index = "some_index",
    doc_type = "_doc"
    )

    # print the response returned by Elasticsearch
    print ("helpers.bulk() RESPONSE:", resp)
    print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

except Exception as err:
    # print any errors returned w
    ## Prerequisiteshile making the helpers.bulk() API call
    print("Elasticsearch helpers.bulk() ERROR:", err)
    quit()
