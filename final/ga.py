""" I am going to keep population size to be 100
then on the 100 population I will apply genetic algo.
In that first I will find errors by sending the requests to the server 
then I will sort it. No select some portion of the population (fittest) and pass it to the next generation
now we have to make childs so cross over and mutation is done"""
import random
import client_moodle
import json
pop_size = 26
initial_randomness = 1e-13
percent_parent = 10
cross_rate = 0.45
overfit_original = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
mutation_range = 1e-13
MAX_DEG = 11
generations = 30
percent_fit = 60 ## these percent many are selected to participate in the crossover to get new gen
f = open("./output_2.txt", "a")
class Chromosome:
    def __init__(self, vector):
        self.chromo = vector
        self.fit = self.fitness()
    def fitness(self):
        ## this function returns an array with the array containing the 2 errors and the fitness of the function calculated
        # print(self.chromo)
        err = client_moodle.get_errors('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', self.chromo)
        
     #### The following function is variable
        fit = err[0] + err[1]
        # fit = (err[1] - err[0]) * (err[1] + err[0])
        err.append(fit)
        
        return(err)
    
        
        
def cross_over(par_1, par_2):
    child = []
    i = 0 # this will help in finding the index
    for x, y in zip(par_1.chromo, par_2.chromo):
        ## getting a random probability for cross over , it acts as cross over rate and mutation rate
        prob = random.random()
        if prob < cross_rate:
            child.append(x)
        elif prob < 2 * cross_rate:
            child.append(y)
        else:
            # here we need a new value but the value can't be any random values 
            # but it should be something related to the value in the original array
            # at this index
            k = overfit_original[i] + random.uniform(-mutation_range,mutation_range)
            child.append(k)
        i = i+1
    return Chromosome(child)


if __name__ == "__main__":
    
    # generate the first set population
    # from the array given 
    f.write("\n")
    f.write("\n")
    
    f.write("population " + str(pop_size) + " initial_randomness " + str(initial_randomness)+ " percent parent " + str(percent_parent) + " cross rate " + str(cross_rate) + " mutation range " + str(mutation_range) + " percent fit " + str(percent_fit) + " Generations " + str(generations))
    f.write("\n")
    pop = [Chromosome(overfit_original)]
    for i in range(1, pop_size):
        l = []
        for j in range(MAX_DEG):
            ## note we are adding randomness to the i-1 to get i
            gene = pop[i-1].chromo[j] + random.uniform(-initial_randomness,initial_randomness)
            l.append(gene)
        pop.append(Chromosome(l)) 
    gen = 1      
    while gen <= generations:

        ## now I will sort the genes according to the increasing 
        # order of their fitness
        pop = sorted(pop, key=lambda x: x.fit[2])
        new_gen = []
         ## now to get the new generation we are going to best 
         # percent parent and rest we will generate after mutation
        size = int((percent_parent* pop_size)/100)
        new_gen.extend(pop[:size]) ## this will take first "size" genes and add it to new_gen
        # now we need to add rest of the childs
        size = pop_size - size
        for _ in range(size):
            # select any random chromosome from the first percent_fit % of the popultion
            n = int((percent_fit * pop_size) / 100)
            p1 = random.choice(pop[:n])
            p2 = random.choice(pop[:n])
            new_gen.append(cross_over(p1, p2))  
         
        ## now population is this new_gen
        print("Generation " + str(gen) + " Training Error " + str(pop[0].fit[0]) + " Validation Error " + str(pop[0].fit[1]) + " Fitness " + str(pop[0].fit[2]))
        
        f.write("Generation " + str(gen) + " Training Error " + str(pop[0].fit[0]) + " Validation Error " + str(pop[0].fit[1]) + " Fitness " + str(pop[0].fit[2]))
        f.write("\n")
        for i in range(MAX_DEG):
            f.write(str(pop[0].chromo[i]) + ", ")
        f.write("\n")       
        pop = new_gen    
        gen += 1  
        ### Let's submit the fittest chromosome till now ###
        submit_status = client_moodle.submit('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', pop[0].chromo)
        assert "submitted" in submit_status
         ### lets put the fittest in a file
    f.close()    
        
            
            
            