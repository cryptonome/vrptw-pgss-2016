import numpy as np
from Customer import Customer
from Visual import Visual
from Depot import Depot

path = '../standard_instances/'

customers = []
    
def import_customers(filename):
    f = open(path + filename, 'r')
    with open(path + filename) as f:
        for i in xrange(6):
            f.next()
        for line in f:
            custList = line.replace('\n', '').split()
            #create temp customer to add to array; shift location so that it is relative to depot at 0,0
            temp = Customer(int(custList[0])-1, int(float(custList[1])) - 40, int(float(custList[2])) - 50, custList[4], custList[5], custList[6], custList[3])
            #print temp
            customers.append(temp)
            
    #print customers  
    return customers   

# ex: import and then show the customers for file C201.txt [living in directory specified by var 'path']
# Visual.plot_customers(Depot(0,0), import_customers("C201.txt"))