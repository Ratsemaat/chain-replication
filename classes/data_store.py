import json
from enum import Enum


class Status(Enum):
    CLEAN = "clean"
    DIRTY= "dirty"

class DataStore:

    def __str__(self):
        return f"Node{self.owner}id{self.id}"
    def __repr__(self):
        return f"Node{self.owner}id{self.id}"

    def __init__(self, id, owner):
        self.id = id
        self.owner = owner
        self.data = []
        self.next = None
        self.prev = None
        self.data_status = {}
    
    def write(self, data):
        self.data_status[data["book"]] = Status.DIRTY
        self.data.append(data)

    def mark_as_clean(self, data):
        self.data_status[data["book"]] = Status.CLEAN

    def get_data_status(self):
        statuses= self.data_status

        return statuses
    def get_owning_node(self):
        return self.owner
    


