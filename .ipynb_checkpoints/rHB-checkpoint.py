import random
import math
from rSH import RandomSH

class RandomHB:
    
    def __init__(self, sample_size, halving_factor, total_budget, min_budget, max_budget, hb_halving_factor, num_hyperparameters, min_sampling_distance):
        self.num_samples = sample_size
        self.gamma = halving_factor
        self.t_budget = total_budget
        self.minB = min_budget
        self.maxB = max_budget
        self.hb_gamma = hb_halving_factor
        self.num_hpar = num_hyperparameters
        self.d = min_sampling_distance
        self.results = []
        
        
    def start(self):
        num_HB_steps = math.floor(math.log(self.num_samples,self.hb_gamma)) + 1 # number of consecutive SH processes
        #print(num_HB_steps)
        
        experiments_list = []
        for i in range(num_HB_steps):
            # find the number of samples and budget for each HB step 
            step_total_samples = math.floor(self.num_samples/(self.hb_gamma**i))
            step_total_budget = math.floor(self.t_budget/num_HB_steps)
            print("\n\n HB step ** ",i," ** ","    Step budget:",step_total_budget, "    Number of samples:",step_total_samples)
            
            #Here, in the original BOHB we would use the samples calculated in one loop iteration (HB steps)
            #  -> as per request we do not model the data via BO
            # we get a new fresh random sample of point in a N-dimesional spaceinstead
            reference_samples = self.gen_samples(step_total_samples, self.num_hpar) # get the random samples for a HB step 
            
            # create a new SH experiment, i.e. calculate ~y for the set of random points given 
            experiments_list.append(RandomSH(step_total_samples, self.gamma, step_total_budget, self.minB, self.maxB, self.num_hpar, reference_samples))
            # run the experiment
            experiments_list[i].run()
            # record the results as a list of vectors with the form (x1,...,xN,~y) 
            results = experiments_list[i].pull_results()
            #add the results to the overall results
            self.results.extend(results)
            print("step:",i," results: ", self.results)
        
    def gen_samples(self,number_samples,dimention):
        samples = []
        for i in range(number_samples):
            sample = self.gen_tested_sample(samples,dimention,self.d)
            samples.append(sample)
            
        #print("Reference samples: ", samples)
        return samples

    def gen_tested_sample(self,samples,dimention,d):
        sub_sample = []
        if len(samples) == 0:
            for i in range(dimention):
                rand_number = random.random()
                sub_sample.append(rand_number)
            return sub_sample
        else:
            passa = False
            while(passa == False):
                passa = True
                for i in range(dimention):
                    rand_number = random.random()
                    sub_sample.append(rand_number)
                for item in samples: # for each item calculate the euclidean distance
                    val = 0
                    for j in range(dimention):
                        val = val + (sub_sample[j]-item[j])**2
                    val = math.sqrt(val)
                    if val < d:  # compate to minimum distance
                        passa = False
                        
            return sub_sample
    
    def pull_results(self):
        return self.results
    
    def pull_best(self):
        last = len(self.results[0])-1
        #print(last)
        best = self.results[0]
        for i in range(len(self.results)):
            if self.results[i][last] < best[last]:
                best = self.results[i]
                    
        return best