
# -*- coding: utf-8 -*-
import base64
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from keras import backend as K
from recognizer.Corrector import Corrector
from recognizer.Extractor import Extractor
from recognizer.TextConverter import TextConverter
import pathlib

app = Flask(__name__,
            static_folder=pathlib.Path('.').absolute() / 'app' / 'static',
            template_folder=pathlib.Path('.').absolute() / 'app' / 'templates')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    K.clear_session()
    image_str = request.get_data().decode("utf-8").split(';')[1].split(',')[1]
    image = readb64(image_str)

    b, g, r = cv2.split(image)
    image = b
    
    width = image.shape[1]
    height = image.shape[0]

    extractor = Extractor()
    textConverter = TextConverter()
    
    try :
    
        if width == 900 and height == 300 :
            letters, spaceIndex = extractor.extract(image,100,1,None,20,1.5) #seuil, dilatation, flou gaussien, bordure
        else :
            letters, spaceIndex = extractor.extract(image,100,2,4,8,2.25)
        
        res = textConverter.convert(letters, spaceIndex, "best.h5")
        res = Corrector(res).correct()
        print("Predicted output : ", res)
        response = res
        K.clear_session()
        
        return response
    
    except :
        
        return "Error "

def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

if __name__ == '__main__':
    app.debug = False
    app.run(port=5000)
