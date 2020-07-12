from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

tf.keras.backend.clear_session()
from tensorflow.keras.preprocessing import image
from tensorflow import keras
from tensorflow.keras import layers
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import os
import numpy as np
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
longitud, altura = 150, 150
cnn = keras.models.load_model('./Modelo/modelo.h5')
cnn.load_weights('./Modelo/pesos.h5')
def predict(file):
  x = load_img(file, target_size=(longitud, altura))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = cnn.predict(x)
  if array[0]<0.2:
    print("pred: Gato")
  else:
    print("pred: Perro")
  return array
predict('prueba.jpg')
predict('prueba2.jpg')
predict('prueba3.jpg')