import json
import re
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

load_dotenv()


class Search:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.es = Elasticsearch('http://localhost:9200')  # <-- connection options need to be added here
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self):
        self.es.indices.delete(index='my_documents', ignore_unavailable=True)
        self.es.indices.create(
            index='my_documents', #
            body={ #
                'mappings': { #
                    'properties': {
                        'embedding': {
                            'type': 'dense_vector',
                            'dims': 384 #
                        }
                    }
                }
            }
        )

    def get_embedding(self, text):
        return self.model.encode(text)

    def clean_text(self, text):
        """Clean up the text to make it more readable."""
        # Replace excessive newlines, tabs, and spaces with a single space
        text = re.sub(r'\s+', ' ', text)  # Replace one or more whitespace characters with a single space
        text = text.strip()  # Remove leading/trailing spaces
        return text

    def insert_document(self, document):
        # Clean up content and summary before indexing
        document['content'] = self.clean_text(document['content'])
        document['summary'] = self.clean_text(document['summary'])

        return self.es.index(index='my_documents', document={
            **document,
            'embedding': self.get_embedding(document['summary']),
        })

    def insert_documents(self, documents):
        operations = []
        for document in documents:
            # Clean up content and summary before indexing
            document['content'] = self.clean_text(document['content'])
            document['summary'] = self.clean_text(document['summary'])

            operations.append({'index': {'_index': 'my_documents'}})
            operations.append({
                **document,
                'embedding': self.get_embedding(document['summary']),
            })
        return self.es.bulk(operations=operations)

    def reindex(self):
        self.create_index()
        with open('transformed1_output.json', 'rt', encoding='utf-8') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents)

    def search(self, **query_args):
        return self.es.search(index='my_documents', **query_args)

    def retrieve_document(self, id):
        return self.es.get(index='my_documents', id=id)
