import random
from concurrent import futures
from multiprocessing import Process
import grpc

import node_pb2
import node_pb2_grpc
from classes.chain import Chain
from classes.data_store import DataStore

network = "localhost"

port_map = {
    1: 50051,
    2: 50052,
    3: 50053,
}

debug = True
flows = ["create_chain", "all", "connection"]


def debug(par, flow="all"):
    if debug and flow in flows:
        print(par)


def get_ip(ide):
    return f"{network}:{port_map[ide]}"


def is_target_alive(target):
    with grpc.insecure_channel(get_ip(target)) as channel:
        try:
            stub = node_pb2_grpc.ChainReplicationServiceStub(channel)
            resp = stub.IsAliveCheck(node_pb2.Empty())
            debug(f"Node with ip {get_ip(target)} is available, response {resp} ", flow="connection")
            return resp and resp.alive
        except grpc._channel._InactiveRpcError as e:
            debug(f"Node with ip {get_ip(target)} is unavailable ", flow="connection")
            return False


class Node(node_pb2_grpc.ChainReplicationService):

    def __init__(self, id):
        self.idx = 1
        self.id = id
        self.data_stores = []
        self.chain = None

        debug(f"id = {self.id}, type = {type(id)}")
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_ChainReplicationServiceServicer_to_server(self, self.server)

        self.server.add_insecure_port(f'{network}:{port_map[self.id]}')
        self.server.start()
        print(f"Node started with ip {network}:{port_map[self.id]}")

    def GetDataStores(self, request, context):
        debug(str(self.data_stores), flow="create_chain")
        if len(self.data_stores) == 0:
            return node_pb2.DataStoreList(data_store_ids=[])
        stores_as_string = str(self.data_stores)[1:][:-1]
        return node_pb2.DataStoreList(data_store_ids=stores_as_string.split(", "))

    def TransferChain(self, request, context):
        debug(request.chain, flow="create_chain")
        self.chain = Chain()
        self.chain.processes = request.chain
        return node_pb2.ChainAcceptedResponse(accepted=True)

    def IsAliveCheck(self, request, context):
        return node_pb2.IsAliveResponse(alive=True)

    def list_chain(self):
        print(repr(self.chain))

    def init_new_data_store(self):
        self.data_stores.append(DataStore(self.idx, self.id))
        self.idx += 1

    def get_target_nodes_data_stores(self, target):
        if target == self.id:
            debug(f"{self.data_stores}", flow="create_chain")
            return self.data_stores
        with grpc.insecure_channel(get_ip(target)) as channel:
            stub = node_pb2_grpc.ChainReplicationServiceStub(channel)
            resp = stub.GetDataStores(node_pb2.Empty())
            debug(f"{resp}", flow="create_chain")

            return resp.data_store_ids

    def get_active_nodes(self):
        # TODO: Make  it parallel
        active_nodes = []
        for k in port_map.keys():
            debug(k)
            if self.id == k:
                debug("id=k")
                active_nodes.append(k)
            else:
                if is_target_alive(k):
                    active_nodes.append(k)
        return active_nodes

    def send_chain(self, target):
        if target == self.id:
            return True

        with grpc.insecure_channel(get_ip(target)) as channel:
            stub = node_pb2_grpc.ChainReplicationServiceStub(channel)
            debug(f"chain: {str(self.chain).split(',')}", flow="create_chain")
            resp = stub.TransferChain(node_pb2.Chain(chain=str(self.chain).split(",")))
            return resp.accepted

    def create_chain(self):
        nodes = self.get_active_nodes()
        debug(f"Active nodes: {nodes}", flow="create_chain")
        stores = []
        for node in nodes:
            nodes_stores = self.get_target_nodes_data_stores(node)
            debug(f"Node {node} stores: {nodes_stores}", flow="create_chain")
            stores.extend(nodes_stores)

        random.Random(42).shuffle(stores)
        debug(f"stores: {stores}, length {len(stores)}", flow="create_chain")

        self.chain = Chain()
        if len(stores) == 0:
            raise RuntimeError("Failed to create the chain. No datastores found.")
        
        self.chain.head = stores[0]
        self.chain.tail = stores[-1]
        self.chain.processes = [str(store) for store in stores]

        all_accepted = True
        # TODO: sent acknowledgement that about chain creation result
        for node in nodes:
            all_accepted = all_accepted and self.send_chain(node)

        if not all_accepted:
            self.chain = None
            raise RuntimeError("Failed to create the chain")

        return

    def get_data_store_by_id(self, id):
        for store in self.data_stores:
            if store.id == int(id):
                return store
        return None

    def WriteData(self, request, context):
        return self.write({'book': request.book, 'price': request.price}, request.id)

    def send_data(self, data, store_id, node_id):
        with grpc.insecure_channel(get_ip(int(node_id))) as channel:
            stub = node_pb2_grpc.ChainReplicationServiceStub(channel)
            resp = stub.WriteData(node_pb2.WriteRequest(
                book=data['book'], price=data['price'], id=store_id))
            return node_pb2.Empty()

    def write(self, data, id=None):
        print(f"Writing {data} to {id}")
        if self.chain is None:
            raise RuntimeError("Chain is not initialized")
        #Only with head
        if id is None:
            id = self.chain.head
            node_id = id[4]
            if node_id == self.id:
                self.write(data, id)
            else:
                return self.send_data(data, id, node_id)

        if id is not None:
            store = self.get_data_store_by_id(id[-1])
            if store is not None:
                store.write(data)
            
            next_store, next_node = self.chain.get_next_store_and_node(id)
            if next_node is not None:
                if next_node == self.id:
                    self.write(data, next_store)
                else:
                    return self.send_data(data, next_store, next_node)
            else:
                return node_pb2.Empty()

