import argparse
import grpc
from classes.node import Node

def assert_par_quantity(pars, quantity):
    if quantity > len(pars):
        raise RuntimeError("Too few parameters passed")
    elif (quantity < len(pars)):
        raise RuntimeError("Too many parameters  passed")


def run(args):
    node = Node(args.node_id)
    while True:
        name = input(f"Node {args.node_id}>")
        pars = name.split()
        if pars[0] == "Local-store-ps":
            try:
                assert_par_quantity(pars, 2)
                amount = int(pars[1])
                for i in range(amount):
                    node.init_new_data_store()
                print(f"{amount} stores successfully created")
            except Exception as e:
                print(e)
        elif pars[0] == "exit":
            try:
                assert_par_quantity(pars, 1)
                exit()
            except Exception as e:
                print(e)
        elif pars[0] == "Create-chain":
            node.create_chain()

        elif pars[0] == "List-chain":
            node.list_chain()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('node_id', type=int)
        args = parser.parse_args()
        run(args)
    except RuntimeError as e:
        print(e)

