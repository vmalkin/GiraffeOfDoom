import random
import math
from decimal import Decimal, getcontext
getcontext().prec = 3

# ####################################################################################
# The Neuron Class. ATechnically it's a perceptron
# ####################################################################################
class Neuron:
    def __init__(self, synapselist, brain):
        # list of synapses upstream from the cell with the format:
        # [cell_number, weight]
        self.synapselist = synapselist
        self.brain = brain # so a cell can actually locate the contents of the cell above.
        self.bias = Decimal(5.0)
        self.inputvalue = Decimal(0.0)          # the sum of all inputs
        self.outputvalue = Decimal(0.0)  # the output of the cell.

    # traditional sygmoid function
    def activationfunction(self):
        # First, A Neuron sums up it's inputs
        for syn in self.synapselist:
            # sum up the upstream cell outputs * by the Weight
            self.inputvalue = self.inputvalue + (Decimal(brain[syn[0]].outputvalue) * Decimal(syn[1]))

        # add the bias value
        self.inputvalue = self.inputvalue + self.bias

        # the actual activation function
        # self.outputvalue = 1/(1 + math.pow(math.e, (-1 * self.inputvalue)))
        self.outputvalue = math.tanh(self.inputvalue)

# ####################################################################################
# Make it go! 1 2,2,2,1 layer network
# ####################################################################################
brain = []
# the input layer
n0 = Neuron([],brain)
n1 = Neuron([],brain)

# the first layer
n2 = Neuron([[0,3],[1,3]],brain)
n3 = Neuron([[0,3],[1,3]],brain)

# the second layer
n4 = Neuron([[2,3],[3,3]],brain)
n5 = Neuron([[2,3],[3,3]],brain)

# the output layer
n6 = Neuron([[4,3],[5,3]],brain)

brain = [n0,n1,n2,n3,n4,n5,n6]

# set up the input values
brain[0].inputvalue = 0
brain[1].inputvalue = 0

for i in range(0,len(brain)):
    brain[i].activationfunction()

for cell in brain:
    print(cell.outputvalue)



