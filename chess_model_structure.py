# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 21:35:47 2020

@author: hoope
"""

from tensorflow import keras
import keras.models as km
import keras.layers as kl
from keras import metrics
import numpy as np
import matplotlib.pyplot as plt

x_train = np.load('x_train_complex.npy', allow_pickle=True)
x_test = np.load('x_test_complex.npy', allow_pickle=True)
sq_from_train= np.load('sq_from_train_complex.npy', allow_pickle=True)
sq_from_test= np.load('sq_from_test_complex.npy', allow_pickle=True)
sq_to_train= np.load('sq_to_train_complex.npy', allow_pickle=True)
sq_to_test= np.load('sq_to_test_complex.npy', allow_pickle=True)


def build_model(x_train, sq_train, epoch, my_batch_size, 
                model_name, cat_acc_file_name,
                loss_file_name):
    """
    Builds and trains a model for predicting the a square to move from or to
    based on an input board

    Parameters
    ----------
    x_train : numpy.array
        Chess board representations 
        MUST have shape (None, 6, 8, 8, 1)
    sq_train : np.array
        One hot encodings of the solution to the input array
        MUST have shape (None, 64, 1)
    epoch : int
    my_batch_size : int
    model_name : str
    history_file_name : str

    Returns
    -------
    trained model

    """
    
    model = km.Sequential()
    model.add(kl.Conv3D(800, kernel_size=(6, 5, 5), 
                               input_shape=(6, 8, 8, 1), activation='tanh'))
    model.add(kl.Conv3D(400, kernel_size=(1, 3, 3), 
                               input_shape=(6, 8, 8, 1), activation='tanh'))
    model.add(kl.Conv3D(200, kernel_size=(1, 1, 1), 
                               input_shape=(6, 8, 8, 1), activation='tanh'))
    model.add(kl.Flatten())
    model.add(kl.Dense(name='output', units=64))
    model.compile(optimizer='rmsprop', 
                         metrics=['accuracy','categorical_accuracy'],
                         loss='mean_squared_error')

    model.fit(x_train, sq_train, epochs=epoch, 
                           batch_size=my_batch_size, verbose=2)
    model.save_weights(model_name+'.hdf5')
    np.save(loss_file_name+'.npy', 
            model.history.history['loss'])
    np.save(cat_acc_file_name+'.npy', 
            model.history.history['categorical_accuracy'])
    return model

model_moveFrom = build_model(x_train, sq_from_train, 25, 500,
            "Kasparov_moveFrom_complex_new_features", 
            "cat_acc_moveFrom_complex_new_features", 
            "loss_moveFrom_complex_new_features")
print(model_moveFrom.evaluate(x_test, sq_from_test))
# model_moveTo = build_model(x_train, sq_to_train, 400, 20, 
#             "Kasparov_moveTo_complex_400", "cat_acc_moveTo_complex_400", 
#             "loss_moveTo_complex_400")