import matplotlib.pyplot as plt
import cv2
import os
import sys


class ImgOpener:

    def load(self, path, fileName, x_size=None, y_size=None):

        try:

            os.chdir(path)
            imgray = cv2.imread(fileName, 0)

            if str(type(imgray)) == "<class 'NoneType'>":
                raise Exception

            if (x_size != None and y_size != None):
                imgray = cv2.resize(imgray, (x_size, y_size))

        except FileNotFoundError:
            print("Error : Directory not found")
            sys.exit(0)

        except Exception:
            print("Error : File not found or extension unknown")
            sys.exit(0)

        return imgray

    def plot(self, img):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        plt.imshow(img, interpolation='nearest', cmap='gray')
        plt.colorbar()
        plt.show()
