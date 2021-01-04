# Handwritten Text Recognition

## Description 
The system is able to recognize handwritten text aswell on a sheet of paper as in the canvas of the interface and export it to a downloadable digital format.
The goal was to build a data processing chain of two steps:
* Ingestion and data preparation
* Supervised learning of an image classification model

The data set used to train our model is [EMNIST](https://www.kaggle.com/crawford/emnist/version/1)

## Requirements
#### Python
You first need to install [Python 3.6.x](https://www.python.org/downloads/release/python-368/)

Then you can install Python dependencies using
* `pip install -r requirements.txt`

If you want to install the packages manually, here's a list:

* [TensorFlow](https://www.tensorflow.org/versions/master/get_started/os_setup.html#download-and-setup)
* [Keras](https://keras.io/#installation)
* [Scikit Learn](https://scikit-learn.org/stable/install.html)
* [NumPy](https://github.com/numpy/numpy/blob/master/INSTALL.rst.txt)
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)
* [SciPy](https://github.com/scipy/scipy/blob/master/INSTALL.rst.txt)
* [Opencv](https://pypi.org/project/opencv-python/3.4.5.20/)

#### Docker & Docker Compose
In order to use [Tensorboard](https://www.tensorflow.org/guide/summaries_and_tensorboard), a visualization tool for Tensorflow, you need to install [docker-compose](https://docs.docker.com/compose/install/).

##### Tensorboard
Tensorboard uses the `tensorboard` folder to display the different metrics.
You'll then need to call the tensorboard callback in the `fit` method as followed :

```python
from keras.callbacks import TensorBoard
...
callbackTensorboard = TensorBoard(
        log_dir = 'tensorboard/{}'.format(time()),
        update_freq = 'batch',
        histogram_freq = 1,
        write_graph = True,
        write_images = True)
...
model.fit(
        trainDataX,
        trainLabelY,
        batch_size = batchSize,
        epochs = epoch,
        callbacks = [callbackTensorboard],
        validation_data = validationData)
...
```

Use the following command to start the Tensorboard container :
* `docker-compose up`

Use the following command to stop the Tensorboard container :
* `docker-compose stop`

#### Flask
Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
You can install Flask using
* `pip install Flask`

#### Ngrok
Download [ngrok](https://ngrok.com) and follow the steps for the installation

## How to run 
Clone the Git repository in your system 
Open a terminal and go into the file which contain the Git repository then type : 
* `cd inge2i-ocr`
* `cd src`

Use the following command to start the Flask app :
* `python app.py`

Then open an other tab in your terminal and type : 
* `./ngrok http 127.0.0.1:5000`

Copy the URL generated (for example  http://abc123.ngrok.io ) and visit the website from your navigator.

## How it looks
![Demo](docs/Test.jpg)



