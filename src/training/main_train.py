# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:49:33 2019

@author: nerri
"""

from Splitter import Splitter
from DataOpener import DataOpener
from ModelGenerator import ModelGenerator
import numpy as np
import os
from pathlib import Path
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf


def augment_data(dataset, dataset_labels, augmentation_factor=1, use_random_rotation=True, use_random_shear=True, use_random_shift=True, use_random_zoom=True):
	augmented_image = []
	augmented_image_labels = []

	for num in range (0, dataset.shape[0]):

		for i in range(0, augmentation_factor):
			# original image:
			augmented_image.append(dataset[num])
			augmented_image_labels.append(dataset_labels[num])

			if use_random_rotation:
				augmented_image.append(tf.contrib.keras.preprocessing.image.random_rotation(dataset[num], 20, row_axis=0, col_axis=1, channel_axis=2))
				augmented_image_labels.append(dataset_labels[num])

			if use_random_shear:
				augmented_image.append(tf.contrib.keras.preprocessing.image.random_shear(dataset[num], 0.2, row_axis=0, col_axis=1, channel_axis=2))
				augmented_image_labels.append(dataset_labels[num])

			if use_random_shift:
				augmented_image.append(tf.contrib.keras.preprocessing.image.random_shift(dataset[num], 0.2, 0.2, row_axis=0, col_axis=1, channel_axis=2))
				augmented_image_labels.append(dataset_labels[num])

			if use_random_zoom:
				augmented_image.append(tf.contrib.keras.preprocessing.image.random_zoom(dataset[num], (0.9,0.9), row_axis=0, col_axis=1, channel_axis=2))
				augmented_image_labels.append(dataset_labels[num])

	return np.array(augmented_image), np.array(augmented_image_labels)

opener=DataOpener()

train = opener.ReadFromCsv(os.path.join(os.getcwd(), '../../data/raw/emnist-letters-train.csv'))
test = opener.ReadFromCsv(os.path.join(os.getcwd(), '../../data/raw/emnist-letters-test.csv'))

split_train=Splitter(train)
split_test=Splitter(test)

X,y = split_train.ProcessData('23',26 , split=False)


X_augmented , y_augmented = augment_data(X,y ,augmentation_factor=3, use_random_shear=False)

X_test,y_test = split_test.ProcessData("1",26, split=False)
validation_data= X_test,y_test

"""
premier model sans augmentation de données
"""
mg = ModelGenerator([])
mg.GenerateBest()

mg.modelArray[0].compile('adam' , 'categorical_crossentropy', metrics=['accuracy'])
result = mg.ModelsTraining(X,y,64,40,1,validation_data)
mg.TrainingHistoriesPlot(result)

"""
on utilise l'augmentation de données *4
"""
mg_with_augmented = ModelGenerator([])
mg_with_augmented.GenerateBest()

mg_with_augmented.compile('adam' , 'categorical_crossentropy', metrics=['accuracy'])
result = mg_with_augmented.ModelsTraining(X_augmented,y_augmented,64,40,1,validation_data)
mg_with_augmented.TrainingHistoriesPlot(result)

"""
on utilise un aurre moyen d'augmentation de données en temps réel, 
coûte moins en terme de puissance de calcul
"""
gen = ImageDataGenerator(rotation_range=10,width_shift=0.1 , height_shift=0.1,zoom_range=0.1)

gen.fit(X)

data_gen = gen.flow(X,y, seed=42)

mg_rt_augmented = ModelGenerator([])
mg_rt_augmented.GenerateBest()

mg_rt_augmented.compile('adam' , 'categorical_crossentropy', metrics=['accuracy'])
result = mg_rt_augmented.fit_generator(data_gen , steps_per_epoch=len(X)/32 , epochs=40 , validation_data=validation_data)
mg_rt_augmented.TrainingHistoriesPlot(result)

