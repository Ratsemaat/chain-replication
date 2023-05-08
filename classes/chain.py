import json
import random


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
        self.deviation=0
        self.removed_head=None

    def remove_head(self):
        if len(self.processes) > 0:
            self.processes.remove(self.head)
            self.removed_head = self.head
            self.deviation = 0
            self.head = self.processes[0]
        else:
            self.head = None
            self.tail = None
            print("There is no head to remove")
            return
    
    def restore_head(self):
        if self.removed_head is None:
            print("There is no head to restore")
            return
        if self.deviation > 5:
            self.deviation = 0
            print("Deviation is too big, the lastly removed head is permanently removed")
            return
        self.processes.insert(0, self.removed_head)
        self.head = self.removed_head
        self.removed_head = None
        self.deviation = 0

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




