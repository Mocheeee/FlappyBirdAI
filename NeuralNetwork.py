import tensorflow as tf
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.utils import normalize
import numpy as np
from configs import *

class NeuralNetModel:
    def __init__(self, weight = None, input_shape= (4,)):
        self.model = Sequential()
        self.model.add(Dense(1 ,input_shape=input_shape, kernel_initializer='normal', activation =tf.nn.sigmoid))
        if weight:
            self.model.set_weights(weight)

    def mutate(self, rate):
        weights = self.model.get_weights()[0]
        bias = self.model.get_weights()[1]

        if np.random.rand(1) <= rate:
            bias += np.random.normal(BIAS_STDEV, BIAS_MEAN,1)

        for i, w in enumerate(weights):
            if np.random.rand(1) <= rate:
                weights[i] += np.random.normal(WEIGHT_STDEV, WEIGHT_MEAN, 1)
        
        self.model.set_weights(np.array([weights, bias]))

    def predict(self, input):
        return self.model.predict(input)

    def clone(self):
        weight = self.model.get_weights()
        new_model = NeuralNetModel(weight)
        return new_model
        