import math

class TestModel:
    # this toy model simply sum the square of all input dimentions and than it is multiplied by a fixed fraction per iteration
    # the value is arbitrary
    
    def __init__(self,sample):
        self.sample = sample
        self.loss = -1 # negative means that it was not assign
        self.iterator_fraction = 0.9
        self.state = self.sum_components(self.sample)  # here the state represent the currest loss in from the system
    
    def sum_components(self,sample):
        val = 0
        for value in sample:
            val = val + value
        return val
    
        
    def get_init_sample(self):
        return self.sample
    
    def get_state(self):
        return self.state
    
    def iterate(self, budget, index):
        # the more one iterate, the smaller is the loss (state)
        print("        >>>> Start iterations for Object: ", index)
        print("        iteration ",end = " ")
        for i in range(budget):
            self.state = self.state * self.iterator_fraction
            print(i, end = " ")
        print("    <<<<")
        
    

        