#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:03:21 2019

@author: Nicholas Fong
"""

import io
import os
import pandas as pd
import re
import time
import nltk
from tqdm import tqdm
nltk.download('wordnet')
# Imports the Google Cloud client library
# pip install google-cloud-vision
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'google_cloud_authentication.json')
# Instantiates a client
client = vision.ImageAnnotatorClient()
lemmatizer = nltk.stem.WordNetLemmatizer()

def extract_label(path):
    m = re.search(r'(\\)(.+)(_)', path)
    return m.group(2)

def get_dataset(directory):
    data = pd.DataFrame(columns=['path', 'class'])
    for path, directories, files in os.walk(directory):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if (file_extension.strip().lower() == '.jpg') or (file_extension.strip().lower() == '.jpeg'):
                label = lemmatizer.lemmatize(extract_label(path))
                row = pd.DataFrame([[os.path.join(path, file), label]], columns=['path', 'class'])
                data = data.append(row, ignore_index=True)
    return data

data = get_dataset('../data/ImageNet')
tags = pd.DataFrame(columns=['tag1', 'score1', 'tag2', 'score2', 'tag3', 'score3', 'tag4', 'score4', 'tag5', 'score5', 'success'])
start_time = time.time()

for i in tqdm(range(len(data))):
    file_name = data.path[i]
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    # Parse labels
    tag_scores = []
    success = 0
    count = 0  # I know this is stupid, but this isn't worth refactoring
    for label in labels:
        tag = lemmatizer.lemmatize(label.description.lower())
        score = label.score
        tag_scores.append(tag)
        tag_scores.append(label.score)
        if tag == data['class'][i] and count < 5:
            success = score
        count += 1
    # Handle when less than 5 tags are returned
    tag_scores = tag_scores[:10]
    while len(tag_scores) < 10:
        tag_scores.append('')
        tag_scores.append(0)
    tag_scores = tag_scores[:10]
    tag_scores.append(success)
    row = pd.DataFrame([tag_scores], columns=['tag1', 'score1', 'tag2', 'score2', 'tag3', 'score3', 'tag4', 'score4', 'tag5', 'score5', 'success'])
    tags = tags.append(row, ignore_index=True)
# Output and display results
end_time = time.time()
print('Time taken: {} seconds'.format(end_time - start_time))
results = data.join(tags)
results.to_csv('../output/google_labels.csv', index=False)
print('Mean Score:', sum(results.success) / len(results))