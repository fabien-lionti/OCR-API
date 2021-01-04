
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:56:29 2019

@author: nerri
"""

from keras.layers import Dense,Conv2D,MaxPooling2D,Dropout,Flatten,BatchNormalization
from keras.models import Sequential,load_model
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, BatchNormalization
import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import TensorBoard
from time import time
import os

callbackTensorboard = TensorBoard(
    log_dir='../../tensorboard/{}'.format(time()),
    update_freq='batch',
    histogram_freq=1,
    write_graph=True,
    write_images=True)


class ModelGenerator:

    def __init__(self, modelArray):
        self.modelArray = []
        return

    def GenerateBest(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=(28, 28, 1)))
        model.add(BatchNormalization())
        model.add(Conv2D(32, kernel_size=3, activation='relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(32, kernel_size=5, strides=2, padding='same', activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(64, kernel_size=3, activation='relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(64, kernel_size=3, activation='relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(32, kernel_size=5, strides=2, padding='same', activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Flatten())

        model.add(Dense(128, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Dense(26, activation='softmax'))
        self.modelArray.append(model)
        return self.modelArray

    def GenerateAll(self):
        self.GenerateByLayers()
        self.GenerateByFeaturesMap()
        self.GenerateByDropout()
        self.GenerateByDenses()

        return self.modelArray

    def GenerateByLayers(self):

        model = [0] * 3

        for i in range(3):
            model[i] = Sequential()
            model[i].add(Conv2D(24, kernel_size=5, padding='same', activation='relu', input_shape=(28, 28, 1)))
            model[i].add(MaxPooling2D(pool_size=(2, 2)))

            if (i > 0):
                model[i].add(Conv2D(48, kernel_size=5, padding='same', activation='relu'))
                model[i].add(MaxPooling2D(pool_size=(2, 2)))
            if (i > 1):
                model[i].add(Conv2D(64, kernel_size=5, padding='same', activation='relu'))
                model[i].add(MaxPooling2D(pool_size=(2, 2)))

            model[i].add(Flatten())
            model[i].add(Dense(256, activation='relu'))
            model[i].add(Dense(26, activation='softmax'))
            self.modelArray.append(model[i])
            print("Model" + str(i) + " géneré")

        return self.modelArray

    def GenerateByFeaturesMap(self):

        model = [0] * 6

        for i in range(6):
            model[i] = Sequential()
            model[i].add(Conv2D(i * 8 + 8, kernel_size=5, padding='same', activation='relu', input_shape=(28, 28, 1)))
            model[i].add(MaxPooling2D(pool_size=(2, 2)))

            model[i].add(Conv2D(i * 16 + 16, kernel_size=5, padding='same', activation='relu'))
            model[i].add(MaxPooling2D(pool_size=(2, 2)))

            model[i].add(Flatten())
            model[i].add(Dense(256, activation='relu'))
            model[i].add(Dense(26, activation='softmax'))
            self.modelArray.append(model[i])

        return self.modelArray

    def GenerateByDenses(self):
        model = [0] * 8
        for j in range(8):
            model[j] = Sequential()
            model[j].add(Conv2D(32, kernel_size=5, activation='relu', input_shape=(28, 28, 1)))
            model[j].add(MaxPooling2D(pool_size=(2, 2)))
            model[j].add(Conv2D(64, kernel_size=5, activation='relu'))
            model[j].add(MaxPooling2D(pool_size=(2, 2)))
            model[j].add(Flatten())
            if j > 0:
                model[j].add(Dense(2 ** (j + 4), activation='relu'))
            model[j].add(Dense(26, activation='softmax'))
            self.modelArray.append(model[j])
        return self.modelArray

    def GenerateByDropout(self):
        model = [0] * 8
        for j in range(8):
            model[j] = Sequential()
            model[j].add(Conv2D(32, kernel_size=5, activation='relu', input_shape=(28, 28, 1)))
            model[j].add(MaxPooling2D(pool_size=(2, 2)))
            model[j].add(Dropout(j * 0.1))
            model[j].add(Conv2D(64, kernel_size=5, activation='relu'))
            model[j].add(MaxPooling2D(pool_size=(2, 2)))
            model[j].add(Dropout(j * 0.1))
            model[j].add(Flatten())
            model[j].add(Dense(256, activation='relu'))
            model[j].add(Dropout(j * 0.1))
            model[j].add(Dense(26, activation='softmax'))
            self.modelArray.append(model[j])
        return self.modelArray

    def ModelsSummary(self):
        print(len(self.modelArray))
        for i in range(len(self.modelArray)):
            print(self.modelArray[i].summary())
        return

    def ModelsCompilation(self):
        for i in range(len(self.modelArray)):
            self.modelArray[i].compile('adam', 'categorical_crossentropy', ['accuracy'])
            print("Model" + str(i) + " Compilé")
            return

    def ModelsTraining(self, predictorsDataTrain, targetDataTrain, batchSize, epochsNbr, verbose, validationData):
        Result = []
        if (len(self.modelArray) == 1):
            Result.append(self.modelArray[0].fit(predictorsDataTrain, targetDataTrain, batchSize, epochsNbr, verbose,
                                                 validation_data=validationData, callbacks=[callbackTensorboard]))
        else:
            for i in range(len(self.modelArray)):
                Result.append(
                    self.modelArray[i].fit(predictorsDataTrain, targetDataTrain, batchSize, epochsNbr, verbose,
                                           validation_data=validationData, callbacks=[callbackTensorboard]))
            # print("CNN {0}: Epochs={1:d}, Train accuracy={2:.5f}, Validation accuracy={3:.5f}".format(
        # names[j],epochs,max(history[j].history['acc']),max(history[j].history['val_acc']) ))

        return Result

    def ModelsEvaluation(self, predictorsDataTest, targetDataTest):
        score = []
        for i in range(len(self.modelArray)):
            score.append(self.modelArray[i].evaluate(predictorsDataTest, targetDataTest))
            print(score[i][1])
        return score

    def FindBestModel(self, predictorsDataTest, targetDataTest):
        score = []
        score = self.ModelsEvaluation(predictorsDataTest, targetDataTest)
        score.sort()
        return np.argmax(score)
    
    def TrainingHistoriesPlot(self, Result, names=None):
        styles=[':','-.','--','-',':','-.','--','-',':','-.','--','-']
        #plot the Loss Curve
        plt.figure(figsize=[8,6])
        for i in range(len(self.modelArray)):
            #plt.plot(Results[i].history['val_loss'],'r',linewidth=3.0)
            plt.plot(Result[i].history['loss'],'b',linestyle=styles[i])
            plt.plot(Result[i].history['val_loss'],'r', linestyle=styles[i])
        if names != None:
            plt.legend(names,loc='upper left')
        
        plt.xlabel('Epochs ',fontsize=16)
        plt.ylabel('Loss',fontsize=16)
        plt.title('Loss Curves',fontsize=16)
        axes=plt.gca()

        return score

    
    
    #Save both model and weights in the same file
    def SaveModel(self , fileName, i , delete=False ):
        self.modelArray[i].save(os.path.join(os.getcwd(), '../../models/') + fileName + '.h5')
        print("Model Saved")
        if(delete == True):
            del modelToSave
        else:
            return
    
    def LoadModel(self , fileName):
        loadedModel = load_model(os.path.join(os.getcwd(), '../../models/') + fileName + '.h5')
        print("Model Loaded")
        return loadedModel
            