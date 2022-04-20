from operator import le
import matplotlib.pyplot as plt
import numpy as np

def genome_to_direction(genome):
    if genome == 0:
        return np.array([0,1])
    elif genome == 1:
        return np.array([1,0])
    elif genome == 2:
        return np.array([0,-1])
    if genome == 3:
        return np.array([-1,0])
    else:
        raise Exception('wrong genome input!')

class Plant:
    
    def __init__(self, genomes, sun_units, root):
        self.genomes = genomes
        self.state = True # True means alive.
        self.sun_units = sun_units # Equivalent to available food
        self.root = root

    def mutate(self):
        loc = np.random.randint(0,len(self.genomes))
        self.genomes[loc] = np.random.randint(0,4)

class Garden:

    def __init__(self, population, length):
        self.population = population
        self.length = length
        self.matrix = np.zeros(shape=(self.length, int(self.length * 0.5), len(self.population)), dtype=bool)

    def get_sun_units(self):
        self.grow_plants()
        for x_unit in range(self.length):
            mtx = self.matrix[x_unit,:,:]
            matrix_height = np.array([[i for j in range(mtx.shape[1])] for i in range(mtx.shape[0])]) * mtx            
            
            if np.max(matrix_height) != 0:

                winner_plant_idxs = np.argwhere(matrix_height == np.max(matrix_height))[:,1]
            
                for winner_plant_idx in winner_plant_idxs:
                    self.population[int(winner_plant_idx)].sun_units += 1 / len(winner_plant_idxs)

        return [plant.sun_units for plant in self.population]

    def grow_plants(self):
        self.matrix = np.zeros(shape=(self.length, int(self.length * 0.5), len(self.population)), dtype=bool)
        for idx, plant in enumerate(self.population):
            pos = np.array([plant.root, 0])
            self.matrix[plant.root, 0, idx] = True
            
            for brick in plant.genomes:
                pos += genome_to_direction(brick)
                
                # Check if the brick of the plant is inside the garden
                if (pos[0] >= 0) and (pos[0] < self.matrix.shape[0]):
                    if (pos[1] >= 0) and (pos[1] < self.matrix.shape[1]):
                        # Add the brick to the garden
                        self.matrix[pos[0], pos[1], idx] = True

    def display(self):
        self.grow_plants()
        image = self.matrix.max(axis=2)
        image = image[:,::-1].T
        plt.figure(figsize=(10,8))
        plt.imshow(image)#, interpolation='nearest')
        plt.xlabel('X-Achse')
        plt.show()


class Evolution:

    def __init__(self, population):
        self.population = population # A list with instances of Plants
        self.population_size = len(population)

    def run(self, generations=100, length_garden=100):
        # Assuming the following steps have already been taken:
        #  - Initialize Population
        #  - Generate random root for each plant
        #  - Generate random genomes for each plant
        
        mygarden = Garden(self.population, length=length_garden)
        mygarden.display()

        for i in range(generations):
            # Calculate fitness of each plant. -> is it dead or alive
            # The calcuation is equivialent to running the simulation.
            fitness = mygarden.get_sun_units()
            
            # All survivors procreate without cross mutation.
            # The number of offsprings each surviving plant gets to have is 
            # anti-proportional to the total number of survivers, e. g. the 
            # population size stayes constant. (or does it? that for later projects)
            old_population = list(np.array(self.population)[np.array(fitness) > np.max(fitness) / 2])

            print(f'# Survivors: {len(old_population)}, mean fitness: {round(np.mean(fitness), 2)}',)
            # print(len(old_population))
            if len(old_population) == 0:
                print(fitness)

            # Rebirth the population in equal parts from the parents.
            population = np.array(old_population * (int(self.population_size / len(old_population)) + 1))[0:self.population_size]

            # The new population is at that point a multiset of copies of the survivors genes.
            # Mutate the genomess of every plant in the population
            for plant in population:
                plant.mutate() # Mutates the genomes
                plant.sun_units = 0
                plant.root = np.random.randint(0, mygarden.length)
            
            # Replant the garden with the new population of plants
            mygarden = Garden(population,  length=length_garden)
        
        print('Len ', len(mygarden.population))
        print(fitness)
        print([plant.root for plant in mygarden.population])
        mygarden.display()

        self.population = mygarden.population
            