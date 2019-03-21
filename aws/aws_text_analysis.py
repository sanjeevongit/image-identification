import io
import os
import sys
import re
import pandas as pd
from tqdm import tqdm

#Input to the jaccard similarity algorithm for comparing
#string of texts with each other
#"aws_text_similarity.csv" have labels and extracted text for each file
input_file = './Results/ResultsText/aws_text_similarity.csv'

#Process line output like this
#
#filename	         extracted_text	        word_label	                   similarity
#.\Data\SVT\00_00.jpg	:dol:hut:tapbeer:	doll house tap beer	           
#.\Data\SVT\00_05.jpg	:1+:daieim:muz1o:	anaheim public library muzeo 241	

def replace_colons(text_list):
    text_list = text_list.strip(":")
    return text_list

# Source: https://stackoverflow.com/a/47016862
def get_jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)

# This code was needed to see the encoding for reading the csv file
with open(input_file) as f:
   print(f)

# the encoding for the file is cp1252
labels = pd.read_csv(input_file, encoding='cp1252')
labels['similarity'] = 0.0

# Do actual text extraction
for i in tqdm(range(len(labels))):
    print("\n")
    words = labels['word_label'][i]
    words = words.lower().split()
    words.sort()
    print("Labels:=>", words)
    labels['word_label'][i] = words
    
    #text_detected = replace_whitespace(labels['extracted_text'][i])
    text_detected = replace_colons(labels['extracted_text'][i])
    text_detected = text_detected.split(':')
    print("Detected text:=>", text_detected)
    labels['extracted_text'][i] = text_detected
    #print(i, "filename:", labels['filename'], "text_detected:", text_detected[i], "words:", words, "\n") 
    labels['similarity'][i] = get_jaccard_similarity(words, text_detected)
    print("similarity:", labels['similarity'][i], "\n")

print('Mean Jaccard Similarity:', sum(labels.similarity)/len(labels))
labels.to_csv('./Results/ResultsText/aws_text_jaccard.csv', index=False)
