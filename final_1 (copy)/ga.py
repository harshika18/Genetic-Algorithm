""" I am going to keep population size to be 100
then on the 100 population I will apply genetic algo.
In that first I will find errors by sending the requests to the server 
then I will sort it. No select some portion of the population (fittest) and pass it to the next generation
now we have to make childs so cross over and mutation is done"""

    
import random
import client_moodle
import json
# with open("./output.json", "r") as fp:
#     input_str = json.load(fp)
    
pop_size = 20
initial_randomness = 1e-11
percent_parent = 60
cross_rate = 0.30
overfit_original = [-1.5203967995467524e-14, 0.26780968729908916, -8.27172061321546, 0.0430669706939522, 0.02951397909182123, 5.290216820584939e-05, -3.160803812037059e-05, -5.4405649382475115e-08, 1.328186457295824e-08, 1.535813692914258e-11, -1.931344751018906e-12]
# overfit_original = [0.111111111111111111,  0.26776653748952367, -8.555416422871106, 0.04306708962374795, 0.02951404363174599, 5.5608569240571374e-05, -3.160803764936898e-05, -5.649560840291235e-08, 1.3281864566057985e-08, 1.535813681352174e-11, -1.931344761547915e-12]
# overfit_original = [-1.4548031263265324e-14, 0.20780968729908914, -6.555398392978992, 0.04306697069395220, 0.02951397909182123, 5.5608568984569373e-05, -3.160803812037059e-05, -5.649561839320198e-08, 1.3281864572958241e-08, 1.535813692914258e-11, -1.931344751018906e-12]
# overfit_original = [-1.5275587632806716e-12, 0.12403174500885672, -6.211941063143014, 0.05412145974967095, 0.03810848157672577, 8.132366117402373e-05, -6.018769143873952e-05, -1.2515858112367457e-07, 3.4840139315713996e-08, 3.976917490025742e-11, -6.702444837407404e-12]
# overfit_original = [-4.084681068915328e-13, 1.2059474972052525e-13, -6.211941063144067, 0.05218897909651054, 0.03810848157723996, -1.259431349011546e-13, -6.0420777778590354e-05, -2.5884426066830413e-14, 3.4840967514630246e-08, 8.652534439941538e-14, -6.66693061255698e-12]
# overfit_original = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
# overfit_original = [-4.4548031263265324e-14, 8.313094660439671e-14, -6.211941063144345, 0.04933903144709126, 0.03810848157722179, -5.856869810963688e-14, -6.0187691673539934e-05, 5.233188559265946e-14, 3.4840990943967084e-08, 9.731409079227429e-14, -6.722113126107979e-12]
# err = client_moodle.get_errors('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', overfit_original)
# print(str(err[0]) +"   "+str(err[1]))
mutation_range = 10
MAX_DEG = 11
generations = 50
percent_fit = 75 ## these percent many are selected to participate in the crossover to get new gen
f = open("./output_8.txt", "a")
class Chromosome:
    def __init__(self, vector):
        self.chromo = vector
        self.fit = self.fitness()
    def fitness(self):
        ## this function returns an array with the array containing the 2 errors and the fitness of the function calculated
        # print(self.chromo)
        err = client_moodle.get_errors('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', self.chromo)
        
     #### The following function is variable
        # fit = err[0] + err[1]
        # fit = pow(err[1] + err[0], 1) + pow(err[1], 1)
        # fit =pow(err[1] - err[0], 4) + pow(err[1] + err[0], 4)
        # fit = pow(0.5,err[0]) + pow(0.5,err[1])
        # fit = err[1] * 10000000 + err[0]
        fit = 0.8 * err[1] + 0.2 * err[0]
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
            sel = random.randint(1,2)
            if sel==1:
                temp=random.uniform(0.9,1.1) * x
                if temp > 10 or temp < -10:
                    temp = x
                k = temp
                # k = x + pow(10,-i-1) + random.uniform(-initial_randomness, initial_randomness)
            else:
                temp=random.uniform(0.9,1.1) * y
                if temp > 10 or temp < -10:
                    temp = y
                k = temp
                # k = y + pow(10,-i-1) + random.uniform(-initial_randomness, initial_randomness)
            # k = random.uniform(-mutation_range,mutation_range)
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
            ## note we are adding randomness to the 0 to get i
            gene = pop[0].chromo[j] + random.uniform(-initial_randomness,initial_randomness)
            l.append(gene)
        pop.append(Chromosome(l)) 
    # pop = [Chromosome([-1.4908696449833862e-14, 8.313094660439671e-14, -6.211941063144345, 0.04933903144709126, 0.03810848157715883, -5.723025975542263e-14, -6.0187691673539934e-05, -8.552181673261688e-14, 3.4840990943967084e-08, 6.255817490194451e-14, -6.722113126107979e-12])]
    # pop.append(Chromosome([-8.267667770282449e-13, 0.12403174500686437, -6.211941063144853, 0.04933903144753296, 0.038108481576202204, 8.132366067079526e-05, -6.018769149038425e-05, -1.2515778664175447e-07, 3.484115537603841e-08, 4.063999060866369e-11, -6.697974842514821e-12])) 
    # pop.append(Chromosome([-0.12594494021800903, 0.1230888919290818, -6.17759151384157, 0.04710206364174068, 0.03658777752555537, 7.261861388065707e-05, -5.7283668008272463e-05, -1.180649040549302e-07, 3.3150080795214636e-08, 3.958215555612369e-11, -6.385644036865971e-12]))
    # pop.append(Chromosome([2.2293177695760457e-14, 1.1835469336201418e-13, -6.21194106314439, 0.04933903144703784, 0.03810848157723996, -1.0886851973803787e-13, -6.018769158354757e-05, -2.3347484532026432e-14, 3.4840967514630246e-08, 8.283622397169725e-14, -6.713268807230988e-12]))
    # pop.append(Chromosome([2.7688454697278162e-15, 0.12403174500785775, -6.211941063144254, 0.049339031447023944, 0.03810848157710052, 8.132366105894274e-05, -6.018769153293641e-05, -1.2515850459147e-07, 3.4840988298980016e-08, 4.151881663612943e-11, -6.694439601494025e-12]))
    # pop.append(Chromosome([-4.4548031263265324e-14, 8.313094660439671e-14, -6.211941063144345, 0.04933903144709126, 0.03810848157722179, -5.856869810963688e-14, -6.0187691673539934e-05, 5.233188559265946e-14, 3.4840990943967084e-08, 9.731409079227429e-14, -6.722113126107979e-12]))
    # pop.append(Chromosome([-4.6666700910497803e-14, 0.12403174500787496, -6.21194106314443, 0.04933903144700366, 0.038108481577248464, 8.132366088592054e-05, -6.018769163517544e-05, -1.251586291190591e-07, 3.4840870637254675e-08, 4.151524040119759e-11, -6.684095119578374e-12]))
    # pop.append(Chromosome([-7.905678683837179e-14, 7.776309843003387e-12, -6.211941063144327, 0.04933903144703067, 0.03810848157719586, 8.132366092529353e-05, -6.018769154414974e-05, -1.2515865532830672e-07, 3.484106287445039e-08, 4.1525261694990076e-11, -6.70272180910328e-12]))
    # pop.append(Chromosome([6.65449143170301e-14, 7.87321874146915e-12, -6.211941063144429, 0.049339031447191005, 0.03810848157721995, 8.132366089819378e-05, -6.0187691690030825e-05, -1.25158606720246e-07, 3.484087815391896e-08, 4.1521276502230014e-11, -6.69353799213217e-12]))
    # pop.append(Chromosome([-8.179569613112185e-14, 7.838749270783235e-12, -6.2119410631443, 0.04933903144705106, 0.0381084815772366, 8.132366106016847e-05, -6.0187691708911854e-05, -1.2515850616905218e-07, 3.48408661587522e-08, 4.151679201625183e-11, -6.691839872321618e-12]))
    # pop.append(Chromosome([-6.527739133038815e-13, 0.12403174500774226, -6.211941063144333, 0.049339031446893576, 0.03810848157715883, 8.132366095401165e-05, -6.018769229965379e-05, -1.2515852255385648e-07, 3.4840749863103283e-08, 4.0710236599410396e-11, -6.6990543881656824e-12]))
    # pop.append(Chromosome([-7.500340745402818e-14, 0.12403174500779325, -6.2119410631443195, 0.049339031447027434, 0.038108481577247194, 8.132366091966578e-05, -6.0187691513386834e-05, -1.2515848044157443e-07, 3.48410621033073e-08, 4.151492758124411e-11, -6.682039990509282e-12]))
    # pop.append(Chromosome([9.250992438547322e-14, 0.1240317450076866, -6.211941063144319, 0.0493390314470081, 0.038108481577242816, 8.132366089105216e-05, -6.018769153170983e-05, -1.2515864700887201e-07, 3.484106344990478e-08, 4.151809554714513e-11, -6.685252581663673e-12]))
    # pop.append(Chromosome([6.88615956794783e-14, 0.12403174500781762, -6.211941063144251, 0.0493390314471747, 0.03810848157718259, 4.1685668307076686e-14, -6.0187691666780645e-05, 6.545374648951079e-14, 3.484084551089005e-08, 6.330979191661311e-14, -6.683750045977294e-12]))
    for i in range(len(pop), pop_size):
        l = []
        for j in range(MAX_DEG):
            gene = random.uniform(-mutation_range,mutation_range)
            # gene = pop[i-10].chromo[j] + random.uniform(-initial_randomness, initial_randomness)
            l.append(gene)
        pop.append(Chromosome(l))
        
        
        
    
    
     
     
     
    

    
    # pop = [Chromosome()]
    gen = 1      
    # overfit_original[1] -= 0.124031745
    # overfit_original[5] -= 0.00008132366
    # overfit_original[7] += 1.25158609e-7
    while gen <= generations:
        # with open("./output.json", "r") as fp:
        #     input_str = json.load(fp)
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
        # for _ in range(size):
        #     # select any random chromosome from the first percent_fit % of the popultion
        #     n = int((percent_fit * pop_size) / 100)
        #     p1 = random.choice(pop[:n])
        #     p2 = random.choice(pop[:n])
        #     new_gen.append(cross_over(p1, p2))  
        ## now generating the child chromosome,  no of chromosome needed to be produced is size
        ## using adjacent parents
        for i in range(0, 2 *size, 2):
            p1 = pop[i]
            p2 = pop[i+1]
            new_gen.append(cross_over(p1, p2))
        
        
        
        ## now population is this new_gen
        print("Generation " + str(gen) + " Training Error " + str(pop[0].fit[0]) + " Validation Error " + str(pop[0].fit[1]) + " Fitness " + str(pop[0].fit[2]))
        # for i in range(pop_size):
        #     input_str.append(pop[i])
            
            
        
        # with open("./output.json", 'w') as fp_3:
        #     json.dump(input_str, fp_3, indent=2)
       
        for k in range(pop_size):
            with open("./output2.json", "r+") as f1:
                diction = [{"Chromosome" : str(pop[k].chromo), "Error" : str(pop[k].fit)}]
                data = json.load(f1)
                data.update(diction)
                f1.seek(0)
                json.dump(data, f1, indent = 2)
            
        
        
        
        f.write("Generation " + str(gen) + " Training Error " + str(pop[0].fit[0]) + " Validation Error " + str(pop[0].fit[1]) + " Fitness " + str(pop[0].fit[2]))
        f.write("\n")
        for i in range(MAX_DEG):
            f.write(str(pop[0].chromo[i]) + ", ")
        f.write("\n")       
        gen += 1  
        ### Let's submit the fittest chromosome till now ###
        for i in range(10):
            # if(pop[i].fit[0] + pop[i].fit[1] <= 1780000.0 and pop[i].fit[0] + pop[i].fit[1] >= 1400000.0):
            submit_status = client_moodle.submit('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', pop[i].chromo)
            assert "submitted" in submit_status
        ### lets put the fittest in a file
        # arr = []
        # p = True
        # for i in range(pop_size):
        #     if(new_gen[i].fit[2] <= 1780000.0 and new_gen[i].fit[2] >= 1400000.0):
        #         arr.append(new_gen[i])
        #         p = False
        # if(p == True): 
        #     f.close() 
        #     exit()
        # for i in range(len(arr), pop_size):
        #     l = []
        #     for j in range(MAX_DEG):
        #         l.append(arr[0].chromo[j] + random.uniform(-initial_randomness, initial_randomness))
        #     arr.append(Chromosome(l))

        pop = new_gen  
        # pop = arr  
    f.close()    
        
            
            
            