import random
import math
from decimal import Decimal, getcontext
getcontext().prec = 3

# ####################################################################################
# The Neuron Class. ATechnically it's a perceptron
# ####################################################################################
class Neuron:
    def __init__(self):
        # list of synapses upstream from the cell with the format:
        # [cell_number, weight]
        self.bias = Decimal(5.0)
        self.inputvalue = Decimal(0.0)          # the sum of all inputs
        self.outputvalue = Decimal(0.0)  # the output of the cell.

    # traditional sygmoid function
    def activationfunction(self):
        # add the bias value
        self.inputvalue = self.inputvalue + self.bias

        # the actual activation
        self.outputvalue = 1/(1 + math.pow(math.e, (-1 * self.inputvalue)))

        # # tanh as activation function
        # self.outputvalue = math.tanh(self.inputvalue)


    # ####################################################################################
# The Synpase Class.
# ####################################################################################
class Synapse():
    def __init__(self,upstream, downstream, weight):
        self.cellupstream = upstream # the index of the cell upstream
        self.celldownstream = downstream # the index of the cell downstream
        # self.weight = Decimal(random.uniform(0,1))
        self.weight = Decimal(weight)

# ####################################################################################
# Make it go!
# ####################################################################################


# ####################################################################################
# Set up Neurons
# cells 0,1 are input
# cell 6 is output
# ####################################################################################
cells = []
cellnumber = 7 # the number of cells
for i in range(0, cellnumber):
    braincell = Neuron()
    cells.append(braincell)

# ####################################################################################
# Set up Synapses. The total number is equal to the number of cells in one layer
# multiplied by the No of cells in next layer
# this is hardcoded at the moment but we need to come up with a way to automate this
# ####################################################################################

# a 2,2,2,1 layer network
syn0 = Synapse(0, 2, 3)
syn1 = Synapse(0, 3, 3)
syn2 = Synapse(1, 2, 3)
syn3 = Synapse(1, 3, 3)

syn4 = Synapse(2, 4, 3)
syn5 = Synapse(2, 5, 3)
syn6 = Synapse(3, 4, 3)
syn7 = Synapse(3, 6, 3)

syn8 = Synapse(4, 6, -3)
syn9 = Synapse(5, 6, -3)

# synapses are placed into layers...
synlayer0 = [syn0, syn1, syn2, syn3]
synlayer1 = [syn4, syn5, syn6, syn7]
synlayer2 = [syn8, syn9]

# ####################################################################################
# save the state of the brain to file so it can be reloaded.
# ####################################################################################
def saveneurons(celllist):
    pass

def savesynapse(synapselist):
    pass

c1 = 1
c2 = 1
cells[0].bias = 0
cells[1].bias = 0
# set input values...
cells[0].inputvalue = c1
cells[1].inputvalue = c2
cells[0].outputvalue = c1
cells[1].outputvalue = c2


# Polling each synapse determines if the upstream cell has fired, of so, then
# take this value, multiply by the synapse weight, the pass this to downstream cells
# input value
def feedforward(synlayer):
    # take the output from upstream, multiply by weight, add onto input downstream
    for syn in synlayer:
        adjweight = Decimal(cells[syn.cellupstream].outputvalue) * Decimal(syn.weight)
        print(adjweight)
        cells[syn.celldownstream].inputvalue = Decimal(cells[syn.celldownstream].inputvalue) + adjweight


# ####################################################################################
# Adjust the weights in the network to "learn"
# ####################################################################################
def backprop():
    pass

# Take inputs and process thru the layers.
cells[0].activationfunction()
cells[1].activationfunction()
feedforward(synlayer0)

cells[2].activationfunction()
cells[3].activationfunction()
feedforward(synlayer1)


cells[4].activationfunction()
cells[5].activationfunction()
feedforward(synlayer2)
cells[6].activationfunction()


# just printing the neuron values to see if they match with Excel model.
print("")
for cell in cells:
    print(cell.outputvalue)



