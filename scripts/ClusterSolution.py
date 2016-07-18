## Cluster Optimal Solution
## Hard coded cluster solutions
from Path import Path
from Customer import Customer
from Truck import Truck
from Cluster import Cluster

class ClusterSolution():
    def __init__(self, cluster_id, customers, optimal_solution = None, sum_cargo = None, radius = None, center = None):
        self.customers = customers
        self.sum_cargo = sum_cargo
        self.optimal_solution = optimal_solution
        self.cluster_id = cluster_id
        self.radius = radius
        self.center = center
        self.cluster = Cluster(customers)
        self.custom_solution()

    def custom_solution(self):
        self.optimal_solution = self.cluster.get_solution(self.customers)
        self.sum_cargo = self.cluster.get_cargo()
        self.radius = self.cluster.get_radius()
        self.center = self.cluster.get_center()