import grpc

import grpc

from classes.data_store import DataStore

class Node:

    def __init__(self, id):
        self.idx=1
        self.id = id
        self.data_stores = []

    def init_new_data_store(self):
        self.data_stores.append(DataStore(self.idx))
        self.idx+=1





