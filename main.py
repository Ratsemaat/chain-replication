import re
import argparse
import grpc

from classes.data_store import Status
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
        print(f"cmd = {cmd}, p_args = {p_args}")
        try:
            if cmd == "Local-store-ps":
                assert_par_quantity(p_args, 1)
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
                assert_par_quantity(p_args, 0)
                node.list_books()

            elif cmd == "Read-operation":
                assert_par_quantity(p_args, 1)
                cleaned = pars[1].replace('"', '')
                node.read(cleaned)

            elif cmd == "Write-operation":
                assert_par_quantity(p_args, 1)
                cleaned = p_args[0].replace(
                    '<', '').replace('>', '').replace('"', '').split(',')
                book, price = str(cleaned[0]), float(cleaned[1])
                node.write({"book": book, "price": price})

            elif cmd == "Data-status":
                for k,v in  node.get_data_status().items():
                    print(f"{k}: {'clean' if (v==True or v is Status.CLEAN) else 'dirty'}")

            elif cmd == "Remove-head":
                assert_par_quantity(p_args, 0)
                node.remove_head()

            elif cmd == "Restore-head":
                assert_par_quantity(p_args, 0)
                node.restore_head()

            else:
                print(f"Invalid command: '{cmd}'")
        except ValueError as e:
            print("Bad number of arguments." + str(e))


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('node_id', type=int)
        args = parser.parse_args()
        run(args)
    except RuntimeError as e:
        print(e)
