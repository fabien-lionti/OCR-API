from DataOpener import DataOpener
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
import pandas as pd
import tensorflow as tf


class Splitter:

    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def GetPredictorsAndTarget(self, targetColumnName):
        X = self.dataFrame.drop(columns=targetColumnName)
        y = self.dataFrame[targetColumnName]
        return X, y

    def RotateData(self, X):
        X = X.values
        X = X.reshape(X.shape[0], 28, 28)
        for i in range(X.shape[0]):
            X[i] = np.fliplr(X[i])
            X[i] = np.rot90(X[i], axes=(0, 1))
        X = X.reshape(X.shape[0], 784)
        X = pd.DataFrame(X)
        return X 
    
    def OneHotEncoder(self, y_train , targetDifferentValuesNumber ,y_test=None  ):
        y_train=y_train-1
        y_train=to_categorical(y_train,targetDifferentValuesNumber)
        if y_test != None:
            y_test=y_test-1
            y_test=to_categorical(y_test,targetDifferentValuesNumber)
            return y_train, y_test
        else:
            return y_train
        

    def SplitData(self, XPredictors, yTarget):
        X_train, X_test, y_train, y_test = train_test_split(XPredictors, yTarget, train_size=0.8, test_size=0.2)
        X_train = X_train.values
        X_test = X_test.values
        y_train = y_train.values
        y_test = y_test.values
        return X_train, X_test, y_train, y_test

    def SeeImage(self, X_test, y_test):
        imageIndex = np.random.randint(0, X_test.shape[0])

        plt.figure(figsize=[5, 5])
        X_test = X_test.reshape(X_test.shape[0], 28, 28)
        plt.imshow(X_test[imageIndex, :, :], cmap='gray')
        plt.title("Ground Truth : {}".format(y_test[imageIndex]))
        X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
        return
    
    def ProcessData(self , targetColumnName , targetDifferentValuesNumber, rotate=True , split=True , scale=True , augment=False):
        X,y = self.GetPredictorsAndTarget(targetColumnName)
        if rotate:
            X = self.RotateData(X)
        
        if scale:
            X=X/255
        
            
        if split:
            X_train, X_test, y_train, y_test = self.SplitData(X,y)
            
            X_train=X_train.reshape(X_train.shape[0],28,28,1)
            X_test=X_test.reshape(X_test.shape[0],28,28,1)
            
            if augment:
                X_train,y_train = self.AugmentData(X,y,augmentation_factor=3 , use_random_shear=False)
                
            y_train,y_test = self.OneHotEncoder(y_train, targetDifferentValuesNumber,y_test)
        
            self.SeeImage(X_test,y_test)
        
            return X_train,X_test,y_train,y_test
        
        else: 
            X=X.values
            y=y.values
            X=X.reshape(X.shape[0],28,28,1)
            if augment:
                X,y=self.AugmentData(X,y,augmentation_factor=3 , use_random_shear=False)
                
            y = self.OneHotEncoder(y,targetDifferentValuesNumber)
            
            
            self.SeeImage(X,y)
            
            return X,y
    
    def AugmentData(self , X , y , augmentation_factor=1 , use_random_rotation=True, use_random_shear=True , use_random_shift=True , use_random_zoom=True):
        augmented_X = []
        augmented_y =[]
        
        for num in range(0,X.shape[0]):
            for i in range(0,augmentation_factor):
                
                augmented_X.append(X[num])
                augmented_y.append(y[num])
                
                if use_random_rotation:
                    augmented_X.append(tf.contrib.keras.preprocessing.image.random_rotation(X[num]) ,20, row_axis=0 , col_axis=1 , channel_axis=2,fill_mode='nearest',cval=0.0)
                    augmented_y.append(y[num])
                    
                if use_random_shear:
                    augmented_X.append(tf.contrib.keras.preprocessing.image.random_shear(X[num]) , 0.1 , row_axis=0 , col_axis=1 , channel_axis=2,fill_mode='nearest',cval=0.0)
                    augmented_y.append(y[num])
                    
                if use_random_shift:
                    augmented_X.append(tf.contrib.keras.preprocessing.image.random_shift(X[num]) , 0.1,0.1 , row_axis=0 , col_axis=1 , channel_axis=2,fill_mode='nearest',cval=0.0)
                    augmented_y.append(y[num])
                    
                if use_random_zoom:
                    augmented_X.append(tf.contrib.keras.preprocessing.image.random_zoom(X[num]) , (0.9,0.9) , row_axis=0 , col_axis=1 , channel_axis=2,fill_mode='nearest',cval=0.0)
                    augmented_y.append(y[num])
                    
                return np.array(augmented_X) , np.array(augmented_y)
            
