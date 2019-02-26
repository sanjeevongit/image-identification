#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Labels the input image
Created on Thu Feb 14 18:03:21 2019

@author: Nicholas Fong
"""

import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google_cloud_authentication.json"

# Imports the Google Cloud client library
# pip install google-cloud-vision
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = '../data/declaration_of_independence.jpg'

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)










