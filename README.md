# chain-replication
Homework in the course Distributed System at University of Tartu

## Quick startup 
Run three python progams:

    python main.py 1
    python main.py 2
    python main.py 3


## Available commands

|     command      | parameters |              description               | 
|:----------------:|:----------:|:--------------------------------------:|
|  Local-store-ps  |     n      |        Initalizes n data stores        |
|  Create-chain    |     -      |             Creates chain              |
|   List-chain   |     -      |            Prints the chain            |
|    Write-operation    |    <title,price>    |    Writes data to head of the chain    |
|    List-books   |     -      |         List contents of chain         |
|  Read-operation   |     title      | Reads data from one of the chain links |
|   Data-status   |     -      |        Outputs the data status         |
| Remove-head |     -      |              Removes head              |
| Restore-head |     -      |             Restores head              |

## Architecture


Our system consists of three nodes, each of which has a gRPC server that listens for incoming requests from other nodes in the network. In principle our application generalizes for networks with more nodes, but for this demo solution, we only looked at the case with 3 nodes.<br>

The **Node** class is the main class that represents each node in the network and contains the methods that implement the functionality of the system. Whenever a data store wants to exchange info with nearby data stores, it goes through the parent node. <br>

The **Chain** class stores information about the chain of data stores in the network. Each node has access to the chain to retrieve information about the chain's topology.  <br>

The **DataStore** class is used to store data in the system. Each node can have any number of data stores, which are during the chain creation randomly ordered.<br>
![image](https://user-images.githubusercontent.com/37042229/236919717-e4a24ed1-85d4-4b1b-a871-801ae53d8698.png)
