import json

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
    
    def write(self, data):
        self.data.append(data)
    
    def get_owning_node(self):
        return self.owner
    


