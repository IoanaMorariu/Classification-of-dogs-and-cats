# -*- coding: utf-8 -*-
"""Morariu Ioana - proiect SI

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BAgNRl-aYvDZ6DSH3bhJw0wXstQK6Vcz

<p>Proiect Sisteme inteligente și învățare automată - Morariu Ioana-Alexandra</p>

---

<h1><b><center>Clasificarea câinilor și a pisicilor</center></b></h1>
"""

# instalarea Kaggle library
!pip install kaggle

# configuratie pentru Kaggle.json
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

"""Importing the Dog vs Cat Dataset from Kaggle"""

# Kaggle api
!kaggle competitions download -c dogs-vs-cats

!ls

# extragerea datelor din zip
from zipfile import ZipFile

dataset = '/content/dogs-vs-cats.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print('Datele au fost extrase cu succes')

from zipfile import ZipFile

dataset = '/content/train.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print('Datele au fost extrase cu succes')

import os
# numararea fisierelor din folderul train
path, dirs, files = next(os.walk('/content/train'))
file_count = len(files)
print('Number of images: ', file_count)

file_names = os.listdir('/content/train/')
print(file_names)

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from google.colab.patches import cv2_imshow

# afisarea unei imagini cu catel
img = mpimg.imread('/content/train/dog.8957.jpg')
imgplt = plt.imshow(img)
plt.show()

# afisarea unei imagini cu pisica
img = mpimg.imread('/content/train/cat.6472.jpg')
imgplt = plt.imshow(img)
plt.show()

file_names = os.listdir('/content/train/')

for i in range(5):

  name = file_names[i]
  print(name[0:3])

file_names = os.listdir('/content/train/')

dog_count = 0
cat_count = 0

for img_file in file_names:

  name = img_file[0:3]

  if name == 'dog':
    dog_count += 1

  else:
    cat_count += 1

print('Number of dog images =', dog_count)
print('Number of cat images =', cat_count)

#cream un director pentru imaginile pe care le dam resize
if not os.path.exists('/content/image resized'):
  os.mkdir('/content/image resized')

original_folder = '/content/train/'
resized_folder = '/content/image resized/'

for i in range(2000):

  filename = os.listdir(original_folder)[i]
  img_path = original_folder+filename

  img = Image.open(img_path)
  img = img.resize((224, 224))
  img = img.convert('RGB')

  newImgPath = resized_folder+filename
  img.save(newImgPath)

file_names_for_dogs = os.listdir('/content/image resized')

for i in range(5):

  name = file_names[i]
  print(name)

# display resized dog image
img = mpimg.imread('/content/image resized/dog.10872.jpg')
imgplt = plt.imshow(img)
plt.show()

# display resized cat image
img = mpimg.imread('/content/image resized/cat.9189.jpg')
imgplt = plt.imshow(img)
plt.show()

"""**Crearea de etichete pentru imaginile cu caini si pisici**

Cat -> 0
Dog -> 1
"""

# asignam etichetele
filenames = os.listdir('/content/image resized/')


labels = []

for i in range(2000):

  file_name = filenames[i]
  label = file_name[0:3]

  if label == 'dog':
    labels.append(1)

  else:
    labels.append(0)

print(filenames[0:5])
print(len(filenames))

print(labels[0:5])
print(len(labels))

values, counts = np.unique(labels, return_counts=True)
print(values)
print(counts)

"""Converting all the resized images to numpy arrays"""

import cv2
import glob

image_directory = '/content/image resized/'
image_extension = ['png', 'jpg']

files = []

[files.extend(glob.glob(image_directory + '*.' + e)) for e in image_extension]

dog_cat_images = np.asarray([cv2.imread(file) for file in files])

print(dog_cat_images)

type(dog_cat_images)

print(dog_cat_images.shape)

X = dog_cat_images
Y = np.asarray(labels)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

# scalarea datelor
X_train_scaled = X_train/255

X_test_scaled = X_test/255

print(X_train_scaled)

"""# New Section

**Building the Neural Network**
"""

import tensorflow as tf
import tensorflow_hub as hub

mobilenet_model = 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4'

pretrained_model = hub.KerasLayer(mobilenet_model, input_shape=(224,224,3), trainable=False)

num_of_classes = 2

model = tf.keras.Sequential([

    pretrained_model,
    tf.keras.layers.Dense(num_of_classes)

])

model.summary()

model.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics = ['acc']
)

model.fit(X_train_scaled, Y_train, epochs=5)

score, acc = model.evaluate(X_test_scaled, Y_test)
print('Test Loss =', score)
print('Test Accuracy =', acc)

"""**Predictive System**"""

input_image_path = input('Scrie calea')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (224,224))

input_image_scaled = input_image_resize/255

image_reshaped = np.reshape(input_image_scaled, [1,224,224,3])

input_prediction = model.predict(image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)

print(input_pred_label)

if input_pred_label == 0:
  print('The image represents a Cat')

else:
  print('The image represents a Dog')

input_image_path = input('Tasteaza calea')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (224,224))

input_image_scaled = input_image_resize/255

image_reshaped = np.reshape(input_image_scaled, [1,224,224,3])

input_prediction = model.predict(image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)

print(input_pred_label)

if input_pred_label == 0:
  print('The image represents a Cat')

else:
  print('The image represents a Dog')