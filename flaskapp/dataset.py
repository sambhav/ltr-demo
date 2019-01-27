import json
import os

class Dataset:

    def __init__(self, name='dataset'):
        """Creates or loads a dataset containining relevance annotations"""
        self.name = name
        self.filename = name+".json"
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as fin:
                self.dataset = json.load(fin)
        else:
            self.dataset = {}

    def __len__(self):
        return len(self.dataset)

    def annotate(self, query, doc, rel): 
        """Store a relevance annotation """
        if query not in self.dataset:
            self.dataset[query] = {}
        docs = self.dataset[query]
        docs[doc] = rel
        self.dump()

    def is_relevant(self, query, doc):
        """True if the document is relevant for the given query, False otherwise"""
        return self.get_relevance(query, doc) > 0

    def get_relevance(self, query, doc):
        """Returns the relevance of the document for the query"""
        if query not in self.dataset:
            return 0 
        if doc not in self.dataset[query]:
            return 0 
        return self.dataset[query][doc]

    def get_docs(self, query):
        """Returns a map with the relevances of the documents given the query"""
        return self.dataset[query] 

    def get_relevant_docs(self, query):
        """Returns the number of relevance documents for the query"""
        count = 0
        for doc in self.get_docs(query):
            if self.is_relevant(query, doc):
                count+=1
        return count

    def get_queries(self):
        """Returns all the query annotated"""
        queries = self.dataset.keys()
        queries.sort()
        return queries

    def dump(self): 
        """Dumps the current dataset on a json file"""
        for query in self.get_queries():
            if self.get_relevant_docs(query) == 0:
                del self.dataset[query] 
        with open(self.filename, 'w') as fout:
            json.dump(self.dataset, fout, indent=4, sort_keys=True)

        
            
        
