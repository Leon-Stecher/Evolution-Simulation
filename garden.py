from threading import current_thread
import numpy as np

class Plant:
    
    def __init__(self, genome, sun_units, root):
        self.genome = genome
        self.state = True # True means alive.
        self.sun_units = sun_units # Equivalent to available food
        self.root = root

class Garden:
    garden_matrix = np.array([]) 
    # A 3d matrix:
    #     - x, z, plant number
    #     - allows for easy checking double occupation of space-unit
    #       using sum(garden_matrix, axis=2)
    #     - allows for easy plotting


    def __init__(self, population):
        self.population = population

    def run_simuation(self, simulation_lenght):
        for i in range(simulation_lenght):
            for plant in self.population:
                # Update garden_matrix - Grow next T's
                # Some Plants don't have engough sun-units and die.
                # Plants that grow outside of the garden must die for
                # simplicity of the simulation.
                pass
            
            # for all space-units occupied by more than one plant:
            #    the smaller plants die.

            # The population is reduced to alive plants

            # sunlight is collected.
            pass

    def grow(self, plant_id, days=None):
        # Updates the garden_matrix.
        plant = self.population[plant_id]
        mtx = self.garden_matrix[:,:,plant_id]
        X = plant.root
        Z = 0
        if days == None:
            days = len(plant.genome)

        # Add vertical bar of the T:
        t_height = plant.genome[0,0]
        mtx = mtx[X, Z:Z + t_height]
        Z += t_height + 1

        # Add the horizontal bar of the T:
        t_width = plant.genome[0,1]
        mtx = mtx[X - (1 + t_width):X - (1 + t_width), Z]
        Z += t_height + 1
        
        for day in range(1, days):
            t_height = plant.genome[day,0]
            t_width = plant.genome[day,1]
            






    def display(self):
        # display the garden as a 2d projection into the x-z-plane
        pass

class Evolution:

    def __init__(self, population):
        self.population = population # A list with instances of Plants
        self.population_size = len(population)

    def run(self, simulation_lenght, generations=100):
        # Assuming the following steps have already been taken:
        #  - Initialize Population
        #  - Generate random root for each plant
        #  - Generate random genome for each plant
        
        mygarden = Garden(self.population, simulation_lenght)

        for i in range(generations):
            # Calculate fitness of each plant. -> is it dead or alive
            # The calcuation is equivialent to running the simulation.
            mygarden.run_simuation(simulation_lenght)
            
            # All survivors procreate without cross mutation.
            # The number of offsprings each surviving plant gets to have is 
            # anti-proportional to the total number of survivers, e. g. the 
            # population size stayes constant. (or does it? that for later projects)

            
            # The new population is at that point a multiset of copies of the survivors genes.
            # Mutate the genomes of every plant in the population
            for plant in self.population:
                plant.mutate() # Mutates the genome
                plant.rebirth() # Resets the Attribute extent. Now the plant is just it's 
                                # root sticking out of the ground.
            
            # Replant the garden with the new population of plants
            mygarden = Garden(self.population, simulation_lenght)
            