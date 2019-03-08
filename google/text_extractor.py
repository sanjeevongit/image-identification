# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 23:32:58 2019

@author: Nicholas Fong
"""

import io
import pandas as pd
import os
import re
import time
from tqdm import tqdm
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'google_cloud_authentication.json')
client = vision.ImageAnnotatorClient()

# Source: https://stackoverflow.com/a/2077906
def replace_whitespace(string):
    return re.sub(r'\s+', ' ', string).strip()

# Source: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/vision/cloud-client/detect/detect.py
# [START vision_text_detection]
def detect_text(path):
    """Detects text in the file."""
    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    descriptions = ''
    for text in texts:
        descriptions = descriptions + ' ' + replace_whitespace(text.description)
    descriptions = descriptions.lower().split()  # Convert to lowercase list
    descriptions = list(set(descriptions))  # Remove duplicates
    descriptions.sort()
    return descriptions

# Source: https://stackoverflow.com/a/47016862
def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)

labels = pd.read_csv('../data/SVT/svt_labels.csv')
labels['Extracted_Text'] = None
labels['similarity'] = 0.0
start_time = time.time()

# Do actual text extraction
for i in tqdm(range(len(labels))):
    words = labels['Words'][i]
    words = words.lower().split()
    words.sort()
    labels['Words'][i] = words
    
    path = '../data/SVT/img/' + labels.Image[i]
    extracted_text = detect_text(path)
    labels['Extracted_Text'][i] = extracted_text
    labels['similarity'][i] = jaccard_similarity(words, extracted_text)

# Output and display results
end_time = time.time()
print('Time taken: {} seconds'.format(end_time - start_time))
print('Mean Jaccard Similarity:', sum(labels.similarity) / len(labels))
labels.to_csv('../output/google_extracted_text.csv', index=False)