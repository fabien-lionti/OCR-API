import numpy as np
import os
from keras.models import load_model
import sys
import pathlib


class TextConverter:

    def __init__(self):

        self.maping = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                       "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def normalizeForCNN(self, letters):

        data = []  # Adapt letters dimension to feed the CNN
        for index in range(len(letters)):
            for y in range(28):
                for x in range(28):
                    data.append(letters[index][y][x])

        lettersNormalize = np.reshape(data, (len(letters), 28, 28, 1))

        return lettersNormalize

    def convert(self, letters, spaceIndex, modelName):

        text = ""
        letters = self.normalizeForCNN(letters)

        modelByFeatureMap2 = load_model(str(pathlib.Path.cwd().parent / 'models' / modelName))
        result = modelByFeatureMap2.predict(letters)

        for index in range(len(result)):

            if index in spaceIndex:
                text += " "

            text += str(self.maping[np.argmax(result[index])])
        text += " "

        return text
