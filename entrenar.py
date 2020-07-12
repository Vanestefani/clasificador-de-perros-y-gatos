from __future__ import absolute_import, division, print_function, unicode_literals
#tesorflow
import tensorflow as tf
from tensorflow.keras.utils import Sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
#Matar procesos de Keras
from tensorflow.python.keras import backend as K
#lIBRERIAS PARA MANIPURAR ACHIVOS EN EL SISTEMA
import os
import numpy as np
import matplotlib.pyplot as plt

K.clear_session()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


#Ubicacion de las imagenes que se van a usar
data_entrenamiento = './data/Entrenamiento'
data_validacion = './data/Validacion'

entrenamiento_gatos_dir = os.path.join(data_entrenamiento, 'Gatos')  # directory with our entrenamientoing cat pictures
entrenamiento_perros_dir = os.path.join(data_entrenamiento, 'Perros') # directory with our entrenamientoing perro pictures
 # directory with our entrenamientoing perro pictures
validacion_gatos_dir = os.path.join(data_validacion, 'Gatos')  # directory with our validation cat pictures
validacion_perros_dir = os.path.join(data_validacion, 'Perros') # directory with our validation perro pictures
num_cats_tr = len(os.listdir(entrenamiento_gatos_dir))
num_dogs_tr = len(os.listdir(entrenamiento_perros_dir))
num_cats_val = len(os.listdir(validacion_gatos_dir))
num_dogs_val = len(os.listdir(validacion_perros_dir))

total_train = num_cats_tr + num_dogs_tr
total_val = num_cats_val + num_dogs_val

print('total training cat images:', num_cats_tr)
print('total training dog images:', num_dogs_tr)
print('total validation cat images:', num_cats_val)
print('total validation dog images:', num_dogs_val)
print("--")
print("Total training images:", total_train)
print("Total validation images:", total_val)

#-----------------------parametros---------------
#Numero de imagenes que toman en cada pasa
batch_size = 128
#Veces que se intera durante el entrenamiento
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

#-------------------Prepar imagenes

##Preparar imagenes de entrenamiento
train_image_generator = ImageDataGenerator( rescale=1./255,rotation_range=45,width_shift_range=.15,height_shift_range=.15,horizontal_flip=True,zoom_range=0.5) # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory= data_entrenamiento,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary'
                                                           )
val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=data_validacion,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')
sample_training_images, _ = next(train_data_gen)
################crear modelo ########
model = Sequential([
   Conv2D(16, 3, padding='same', activation='relu',
           input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Dropout(0.2),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(1)
])
#####Compilar m odelo
model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
##resumen
model.summary()
##Entrenar el modelo
history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)
##Saber indices
print(train_data_gen.class_indices)
##etiquetas
num_classes = 2
##Guardar modelo
##generar modelo
target_dir = './Modelo/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
model.save('./Modelo/modelo.h5')
model.save_weights('./Modelo/pesos.h5')
