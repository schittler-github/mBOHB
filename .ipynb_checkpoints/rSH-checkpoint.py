import random
import math
from model import TestModel

class RandomSH:
    def __init__(self, sample_size, halving_factor, total_budget, min_budget, max_budget, num_hyperparameters, ref_samples):
        self.sample_size = sample_size
        self.gamma = halving_factor
        self.t_budget = total_budget
        self.minB = min_budget
        self.maxB = max_budget
        self.num_hpar = num_hyperparameters
        self.samples = ref_samples
        self.objects = [] # objects is where the "learning" would have been taking place
        self.result = []
        
    def run(self):
        # derived parameters:   num_rounds, sample_budget(per iteration)

        num_halvings = math.floor(math.log(self.sample_size,self.gamma)) # number of halvings given sample and halving factor
        num_rounds = num_halvings + 1
        print("    number of rounds: ",num_rounds)

        round_budget = math.floor(self.t_budget/num_rounds) # budget per round
        print("    budget per round: ",round_budget)

        if( math.floor(round_budget/(self.sample_size)) < self.minB ):
            print("    the budget is too small: please allocate more resourses or lower the number of samples")
    
        else:    
            sample_budget = [] #budget per sample in each round
            samples_inStep = [] # number of samples to keep per step
            for i in range (num_rounds):
                num_samples = math.floor(self.sample_size/(self.gamma**i))
                samples_inStep.append(num_samples)  
                #print(i,halving_factor,num_samples)
                sample_budget.append(math.floor(round_budget/(num_samples)))
            print("    sample budget per round: ",sample_budget)
    
        # TODO: ADD here the stop condition if max_budget is crossed

        #create the model objects

        for i in range(self.sample_size):
            self.objects.append(TestModel(self.samples[i]))
            #print(self.objects[i].get_init_sample())
            #print(self.objects[i].get_state())
       
        # iterations and selection
        index_list = range(len(self.objects))
        for i in range(num_rounds):
            index_list = random.sample(index_list, samples_inStep[i]) # random halvings
            index_list.sort()
            print("    round:",i,"    indexes:",index_list)
            # here we could run in parallel, maybe in "C" cuda?
            for j in index_list:
                self.objects[j].iterate(sample_budget[i], j)

    def pull_results(self):
        results = []
        for i in range(self.sample_size):
            partial_result = self.objects[i].get_state()
            composed_sample = self.samples[i]
            composed_sample.append(partial_result)
            results.append(composed_sample)
            #print(results)
            
        return results
    
    #def flatten(l):
    #    return [item for sublist in l for item in sublist]