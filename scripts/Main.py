from Customer import Customer
from Truck import Truck
from Depot import Depot
from Cluster import Cluster
from Visual import Visual
from Path import Path
from State import State
from AStar import doAStar
from ImportCustomers import import_customers
from ImportSolution import import_solution
from Distances import Distances
from Dijkstra import Dijsktra
from ClusterStore import ClusterStore
import copy
import argparse
try:
    import ipdb
except:
    print "import ipdb skipped because Dan's school is full of jerks"

# Filenames:    C201.txt, C201_wr_solution.txt
# 				RC208.txt, RC208_wr_solution.txt

# sample calls (made from inside the scripts directory):
# python Main.py C201 C201_wr_solution 3 700 591.55
# python Main.py RC208 RC208_wr_solution 3 1000 891.65 --plot

customers = None
depot = None
num_trucks = None
truck_capacity = None

def init(filename):
    global customers, depot

    print "Importing customers..."
    customers = import_customers(filename + ".txt", test_environment )
    print "Calculating distances..."
    Distances.calculate_matrix(customers)
    print "Storing clusters..."
    #ClusterStore.store_clusters(filename, customers)

    depot = Depot(0,0)

def initial_state(filename):
    global customers

    if filename == "nearest_neighbors":
        print "Generating nearest neighbors solution..."
        depot_c = Customer(0, 0, 0, 0, 0, 0, 0)
        c = [depot_c]
        for cust in customers:
            c.append(cust)

        paths = Dijsktra.get_nearest_neighbors_all_trucks(c, depot_c, num_trucks)

        trucks = []
        for k in range(1, num_trucks + 1):
            t = Truck(k, 0, 0, truck_capacity, path = Path(paths[k-1][1:]))
            trucks.append(t)

        state = State( trucks, parent = None )
    
    elif filename == "nn_random":
        print "Generating nearest neighbors random solution..."
        depot_c = Customer(0, 0, 0, 0, 0, 0, 0)
        c = [depot_c]
        for cust in customers:
            c.append(cust)

        paths = Dijsktra.get_nearest_neighbors_random(c, depot_c, num_trucks)

        trucks = []
        for k in range(1, num_trucks + 1):
            t = Truck(k, 0, 0, truck_capacity, path = Path(paths[k-1][1:]))
            trucks.append(t)

        state = State( trucks, parent = None )

    #doesn't work yet, don't use
    elif filename == "split_nearest_neighbors":
        print "Generating split nearest neighbors solution..."
        paths = []
        depot_c = Customer(0, 0, 0, 0, 0, 0, 0)
        
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        # PLEASE DON'T MAKE ANY CHANGES TO THIS PART BELOW
        # UNLESS YOU FIX THE TRUCK NUMBER DEPENDENCY
        # WHILE YOU'RE DOING IT.  THANKS TEAM ;) ;) ;)
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        route1 = [depot_c]
        route2 = [depot_c]
        route3 = [depot_c]
        customers_by_distance = sorted(customers, key=lambda customer: Distances.get_distance(depot_c.number, customer.number) * customer.timewindow())
        for customer in customers_by_distance:
                if customer.x < 0 and customer.y > -15:
                    route1.append(customer)
                elif customer.x >= 0 and customer.y > -15:
                    route2.append(customer)
                else:
                    route3.append(customer)
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################
        ##################################################


        # @TODO truck number dependency
        routes = [ Dijsktra.get_nearest_neighbors( [depot_c], [depot_c][0] ) for x in range( num_trucks ) ]
        state = State( [Truck( k + 1, 0, 0, truck_capacity, path=routes[k] ) for k in range( num_trucks ) ], parent = None)
        state.plot()
    else:
        state = import_solution(filename  + ".txt")

    if do_plot:
        state.plot()

    return state

parser = argparse.ArgumentParser()
parser.add_argument("problem_file")
parser.add_argument("init_solution_file")
parser.add_argument("num_trucks")
parser.add_argument("truck_capacity")
parser.add_argument("world_record_score")
parser.add_argument("--plot", help="plot the map before the main loop engages", action = "store_true")
parser.add_argument("--test", help="looks into the test directory rather than main directory", action = "store_true")
args = parser.parse_args()
problem_file = args.problem_file
init_solution_file = args.init_solution_file
num_trucks = int(args.num_trucks)
do_plot = args.plot
truck_capacity = int(args.truck_capacity)
world_record_score = float( args.world_record_score )
test_environment = args.test

init(problem_file)
state = doAStar(initial_state(init_solution_file), do_plot, world_record_score)
