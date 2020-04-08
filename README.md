# digit-recognizer
### Digit Recognizer Application Using Tensorflow and Pygame

The following packages are needed:
* pygame
* numpy
* tensorflow

### CNN.py
Tensorflow is used to create a convolutional neural network model. The MNSIT database of handwritten digits is used as the dataset for the model. AFter compilation and fitting, the model is saved. The model in this repository has an accuracy score of 0.9965 (60 epochs).  
To learn more about CNN, check out <https://towardsdatascience.com/image-classification-in-10-minutes-with-mnist-dataset-54c35b77a38d>.

### main.py
Pygame is used to create a fullscreen application. The application was designed for 1080p resolution, but should work on other resolutions. The user can draw a digit in the designated drawing surface. On pressing the predict button, the image drawn by the user is converted to 28 x 28 numpy array and then processed. The model is used to predict the digit and the prediction is displayed on the screen.  
If you don't know about pygame and want to learn it, check out <https://www.youtube.com/playlist?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5>.

###### Created by [Soumotanu Mazumdar](https://github.com/FortunateSpy5) and Sayantan Mondal.
