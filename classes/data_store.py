import json

class DataStore:
    def __init__(self, id):
        self.id = id
        self.data = []#self.load_data()
    #boilerplate follows, probably we can delete itexi
        self.filename= "None"

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        return data

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f)

    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value
        self.save_data()

    def delete(self, key):
        del self.data[key]
        self.save_data()
