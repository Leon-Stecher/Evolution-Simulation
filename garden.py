from threading import current_thread
import numpy as np

class Node:
    def __init__(self, parent, height, width, root):
        self.parent = parent
        self.l = height
        self.width = width
        self.root = root
        self.children = []

class Plant:
    
    def __init__(self, genome, sun_units, root):
        self.genome = genome # Is an instance of Node()
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

    def grow(self, plant_id, day):
        
        def new_growth(node, day):
            if day == 0:
                height, width = node.value
                if self.population[plant_id].sun_units <= height + width - 1:
                    # Update self.garden_matrix unless the new T is outside the garden.
                    
                    self.garden_matrix
                    
                else:
                    self.population[plant_id].state = False
                    print('R.I.P.')
                    return
            else:
                for child_node in node.children:
                    new_growth(child_node, day-1)
        
        new_growth(self.population[plant_id].genome, day)



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
            