# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 19:21:50 2019

@author: Nicholas Fong

Identify whether an image has a face or not.
"""

import os
import pandas as pd
import time
from tqdm import tqdm
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'google_cloud_authentication.json')
client = vision.ImageAnnotatorClient()

def get_dataset(directory, classification):
    data = pd.DataFrame(columns=['path', 'face_present', 'face_detected'])
    for path, directories, files in os.walk(directory):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if (file_extension.strip().lower() == '.jpg') or (file_extension.strip().lower() == '.jpeg'):
                row = pd.DataFrame([[os.path.join(path, file), classification, None]], columns=['path', 'face_present', 'face_detected'])
                data = data.append(row, ignore_index=True)
    return data

faces = get_dataset('../data/Faces', True)
false_faces = get_dataset('../data/FERET/100Mammals_n01861778', False)
df = faces.append(false_faces, ignore_index=True)

start_time = time.time()
for i in tqdm(range(len(df))):
    with open(df.path[i], 'rb') as face_file: 
        # Reference: https://cloud.google.com/vision/docs/face-tutorial
        content = face_file.read()
        image = types.Image(content=content)
        response = client.face_detection(image)
        if len(response.face_annotations) > 0:
            df.face_detected[i] = True
        else:
            df.face_detected[i] = False
end_time = time.time()
df.to_csv('../output/google_faces.csv', index=False)
print('Time taken: {} seconds'.format(end_time - start_time))
print('Accuracy:', sum(df['face_present'] == df['face_detected']) / len(df))