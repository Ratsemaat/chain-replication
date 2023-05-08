import json
import random

from classes.data_store import DataStore


class Process:
    def __init__(self, ds: DataStore):
        self.next = None
        self.prev = None
        self.ds = ds

    def get_owning_node(self):
        return self.ds.owner

    def write(self, data):
        self.ds.write(data)
        #TODO implement writing to node
        pass

    def read(self):
        #TODO implement reading
        pass


class Chain:


    def __str__(self):
        c = [str(p) for p in self.processes]
        return ",".join(c)


    def __repr__(self):
        c = [str(p) for p in self.processes]
        if len(c) > 0:
            c[0] += "(head)"
            c[-1] += "(tail)"

        return f'{", ".join(c)}'

    def __init__(self, ):
        self.processes=[]
        self.head=None
        self.tail=None

    def remove_head(self):
        self.processes.remove(self.head)
        if len(self.processes) > 0:
            self.head = self.processes[0]
        else:
            self.head = None
            self.tail = None

    def get_random_node(self):
        idx = random.Random(42).randint(0, len(self.processes)-1)
        print(idx)
        print(self.processes)
        return self.processes[idx]
    
    def get_next_store_and_node(self, node):
        index = -1
        for i in range(len(self.processes)):
            p = self.processes[i]
            if p == node:
                index = i
                break
            
        if index == len(self.processes) - 1:
            return None, None
        return self.processes[index+1], self.processes[index+1][4]




