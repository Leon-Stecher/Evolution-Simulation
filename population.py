from audioop import bias
from cmath import sin
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers


class Individual:
    black_box = object()
    num_links = int()
    genome = object()
    state = bool()

    def __init__(self, num_links = 3):
        self.num_links = num_links
        self.initialize_black_box()

    def get_genome(self):
        genome = self.black_box.weights[0].__array__().ravel()

        for layer_weights in self.black_box.weights[1::]:
            genome = np.concatenate((genome, layer_weights.__array__().ravel()), axis=0)
        
        return genome
    
    def genome_to_black_box(self, genome):
        idx = 0
        for layer in self.black_box.layers[1::]:

            print('\n\n', layer.weights)
            num_layer_weights = layer.weights[0].__array__().ravel().shape[0]
            num_layer_biases = layer.weights[1].__array__().ravel().shape[0]

            # Decode weights from genome:
            weights = genome[idx:idx + num_layer_weights]
            weights = np.reshape(weights, newshape=layer.weights[0].__array__().shape)
            idx += num_layer_weights
            
            # Decode biases from genome:
            biases = genome[idx:idx + num_layer_biases]
            idx += num_layer_biases
            
            layer.set_weights([weights,biases])
        return self.black_box  
        
    def initialize_black_box(self):
        inputs = keras.Input(shape=(self.num_links,))
        # initializer = tf.keras.initializers.Constant(0.5)
        initializer = tf.keras.initializers.RandomNormal(
            mean=0.5, stddev=0.0005, seed=None
        )
        dense = layers.Dense(self.num_links + 1, kernel_initializer=initializer)(inputs)
        outputs = layers.Dense(self.num_links + 1, kernel_initializer=initializer)(dense)

        model = keras.Model(inputs=inputs, outputs=outputs)
        self.black_box = model

    def get_output(self, input):
        output_nn = self.black_box.predict(input)
        return output_nn[0][0:-1], output_nn[0][-1]


class Population:
    # population_size = int()
    graph = list()
    # states = np.array()
    individuals = list()

    def __init__(self, pop_size):
        self.population_size = pop_size
        self.states = np.zeros(shape=(self.population_size))

    def get_output(self, inputs):
        outputs = np.zeros(shape=inputs.shape)
        for i, individual in enumerate(self.individuals):
            m = individual.num_links

            single_output, single_state = individual.get_output(np.expand_dims(np.array(inputs[i * m: i * m + m]), axis=0))

            outputs[i * m: i * m + m] = single_output
            self.states[i] = int(single_state)

        return outputs

    def LINK(self, output):
        # return LINK * Output(I)
        pass
            