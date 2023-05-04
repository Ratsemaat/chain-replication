import argparse

from classes.node import Node


def assert_par_quantity(pars, quantity):
    if quantity > len(pars):
        raise RuntimeError("Too few parameters passed")
    elif (quantity < len(pars)):
        raise RuntimeError("Too many parameters  passed")

def run(args):
    node = Node(args.node_id)
    print("Node started")
    while True:
        name = input(f"Node {args.node_id}>")
        pars = name.split()
        if pars[0] == "Local-store-ps":
            try:
                assert_par_quantity(pars, 2)
                amount = int(pars[1])
                for i in range(amount):
                    node.init_new_data_store()

            except Exception as e:
                print(e)
        elif pars[0] == "exit":
            try:
                assert_par_quantity(pars, 1)
                exit()
            except Exception as e:
                print(e)

            """
            #Stupid boilerplate that maybe can be easily modified, otherwise delete it
            with grpc.insecure_channel("localhost:50051") as channel:
            stub = example_pb2_grpc.ExampleServiceStub(channel)
            response = stub.SayHello(example_pb2.HelloRequest(name=name))
            print(response.message)
            """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('node_id')
    args = parser.parse_args()
    run(args)
