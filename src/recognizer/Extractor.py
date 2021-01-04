# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:22:46 2019

@author: fabie
"""

import cv2
import numpy as np

class Extractor():
    
    def __init__(self) :
        
        self.index = 0
        self.spaceIndex = []
        
    def preProcessing(self,image,kernelSizeBlur):   
        
        if kernelSizeBlur != None :
            image = cv2.blur(image,(kernelSizeBlur,kernelSizeBlur))
            
        image = cv2.Canny(image,50,100)
        ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    
        return image
    
    def postProcessing(self,letter_normalize,border):
        
        letter_normalize = self.normalize(letter_normalize,0)
        letter_normalize = cv2.copyMakeBorder(letter_normalize, border, border, border, border, cv2.BORDER_CONSTANT, value=[0,0,0])
        letter_normalize = cv2.resize(letter_normalize,(28,28)) 
        
        x, letter_normalize = cv2.threshold(letter_normalize,127,255,cv2.THRESH_BINARY)
        
        width = letter_normalize.shape[1] 
        height = letter_normalize.shape[0]
        
        for i in range(height):
            for j in range(width):
                letter_normalize[i][j] = letter_normalize[i][j]/255
        
        return letter_normalize
    
    def avgBlankSpace(self,coord_x) :
        
        totalBlankSpace = 0
        i = 0
        
        for i in range(len(coord_x)-1) :
            totalBlankSpace += coord_x[i+1][0] - coord_x[i][1]
        i+=1
        print("Nombre d'espace : ",i)
            
        try :
            
            return totalBlankSpace/i
            
        except :
            
            return 0
    
    def blankDetector(self,line,coord,avg):
        
        spaceIndex = []
        
        for i in range(len(coord)):   
            if i+1 < len(coord) and avg < coord[i+1][0] - coord[i][1] :
                spaceIndex.append(i)
                
        return spaceIndex
    
    def horizontalProjection(self,image):
   
        y_sum = []    
        y = cv2.reduce(image, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32S) 
        
        for i in range(len(y)): y_sum.append(y[i][0])
                          
        return y_sum

    def horizontalSeparator(self,y) :
    
        y_size = len(y)
        onCaracters = False
        coord = []
        pos = []
    
        for i in range(y_size):
            
            if y[i] > 0.5*np.mean(y) and onCaracters == False :
                pos.append(i)
                onCaracters = True
                
            elif y[i] == 0 and onCaracters == True :
                pos.append(i)
                coord.append(pos)
                pos = []
                onCaracters = False
                
        return coord
    
    def horizontalExtractor(self,image,coord):
    
        width = image.shape[1]
        lines = []
    
        for i in range(len(coord)):
        
            top = coord[i][0]
            bottom = coord[i][1]
            height = bottom - top
            
            line = np.empty((height,width))
            line = image[:width][top:bottom]
            
            lines.append(line)
    
        return lines
    
    def verticalProjection(self,line):
    
        x_sum = []
        x = cv2.reduce(line, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
    
        for i in range(len(x[0])) : x_sum.append(x[0][i])
            
        return x_sum

    def verticalSeparator(self,x):
    
        x_size = len(x)
        onCaracters = False
        coord = []
        pos = []
        print("Vertical mean : "+str(np.mean(x)))
        for i in range(x_size):
    
            if x[i] > 0.5*np.mean(x) and onCaracters == False:
                
                pos.append(i)
                onCaracters = True
                
            elif x[i] == 0 and onCaracters == True:
                pos.append(i)
                coord.append(pos)
                pos = []
                onCaracters = False

        return coord

    def verticalExtractor(self,line,coord,avg):
        
        height = line.shape[0]
        letters = []
        print("Coord : "+str(coord))
        for i in range(len(coord)):
            
            left = coord[i][0]
            right = coord[i][1]
            width = right - left
    
            letter = np.empty((height,width))
            
            for y in range(height) :
                for x in range(left,right) :
                    letter[y][x-left] = line[y][x]
                
            letters.append(letter)
            self.index += 1
            
            if i+1 < len(coord) and avg < coord[i+1][0] - coord[i][1] :
                print("Distance : "+str(coord[i+1][0] - coord[i][1]))
                print("Avg : "+str(avg))
                self.spaceIndex.append(self.index)
                
        self.spaceIndex.append(self.index)
                         
        return letters
    
    def normalize(self,letter,margin):
        
        width = letter.shape[1] 
        height = letter.shape[0]
        bottom = height
        top = 0
        
        for y in range(0,height):
            for x in range(width):
                if letter[y][x] == 255:
                    bottom = y
                    
        for y in range(height-1,0,-1):
            for x in range(width):
                if letter[y][x] == 255:
                    top = y
     
        new_letter = np.zeros((bottom-top+margin*2,width+margin*2))
        
        for y in range(top,bottom) :
            for x in range(width) :
                new_letter[y-top+margin][x+margin] = letter[y][x]
                
                
        return new_letter
    
    def extract(self,image, thresh, kernelSizeDilatation,kernelSizeBlur, border,spaceCoeff):
        
        res = []
        kernel = np.ones((kernelSizeDilatation,kernelSizeDilatation),np.int8)
         
        if thresh == None :
            x,img_original = cv2.threshold(image,0,255,cv2.THRESH_OTSU)
            img_original = 255 - img_original
            
        else:
            x,img_original = cv2.threshold(image,thresh,255,cv2.THRESH_BINARY_INV) 
        
        img_modified = self.preProcessing(image,kernelSizeBlur)
        img_original = cv2.dilate(img_original,kernel,iterations = 1)
        
        y_hist = self.horizontalProjection(img_modified)
        y_coord = self.horizontalSeparator(y_hist)
        
        lines_modified = self.horizontalExtractor(img_modified,y_coord)
        lines_original = self.horizontalExtractor(img_original,y_coord)
        
        for i in range(len(lines_modified)) :
            
            x_hist = self.verticalProjection(lines_modified[i])
            x_coord = self.verticalSeparator(x_hist) 

            avg = self.avgBlankSpace(x_coord)
            self.blankDetector(lines_original[i],x_coord,avg*2)
            letters = self.verticalExtractor(lines_original[i],x_coord,avg*spaceCoeff)
            
            for j in range(len(letters)) :    
                res.append(self.postProcessing(letters[j],border))
                
        return res, self.spaceIndex
        




