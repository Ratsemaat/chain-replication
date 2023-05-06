import argparse
import grpc
from classes.node import Node


def assert_par_quantity(pars, quantity):
    if quantity > len(pars):
        raise ValueError("Too few parameters passed")
    elif (quantity < len(pars)):
        raise ValueError("Too many parameters  passed")


def run(args):
    node = Node(args.node_id)
    while True:
        name = input(f"Node {args.node_id}>")
        pars = name.split()

        cmd = None
        p_args = None
        if len(pars) == 0:
            continue
        elif len(pars) == 1:
            cmd = pars[0]
            p_args = []
        else:
            cmd, p_args = pars[0], pars[1:]

        try:
            if cmd == "Local-store-ps":
                assert_par_quantity(pars, 1)
                amount = int(pars[1])
                for i in range(amount):
                    node.init_new_data_store()
                print(f"{amount} stores successfully created")

            elif cmd == "exit":
                assert_par_quantity(p_args, 0)
                exit()

            elif cmd == "Create-chain":
                assert_par_quantity(p_args, 0)
                node.create_chain()


            elif cmd == "List-chain":
                assert_par_quantity(p_args, 0)
                node.list_chain()


            elif cmd == "List-books":
                # TODO: Implement. Contact head data store and outputs its contents
                raise NotImplementedError

            elif cmd == "Read-operation":
                # TODO: Implement. Ask from random node. Node asks data from head to assure cleanliness?.
                raise NotImplementedError

            elif cmd == "Write-operation":
                # TODO: Implement. Write to head and start to propagate newly written data in chain.
                raise NotImplementedError

            elif cmd == "Data-status":
                # Todo: Not sure how to do that. Probably ask from head and tail and if they are different then it's dirty. Logical clock mby=
                raise NotImplementedError

            elif cmd == "Remove-head":
                # Todo: Remove-head and notify all nodes of the change
                raise NotImplementedError

            elif cmd == "Restore-head":
                # Todo: Probably we need to implement some logical clock that is located at each data-store that keeps track of number of changes that have occured there.
                raise NotImplementedError

            else:
                print(f"Invalid command: '{cmd}'")
        except ValueError as e:
            print("Bad number of arguments." + e)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('node_id', type=int)
        args = parser.parse_args()
        run(args)
    except RuntimeError as e:
        print(e)
