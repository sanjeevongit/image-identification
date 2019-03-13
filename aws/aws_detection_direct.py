import boto3
import os
import sys
import re
import time
import pandas as pd

'''
bucket_name = 'coen241-istore'
s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name)
print('Creating Amazon s3 bucket: ' + bucket_name)
# upload a file to the s3 bucket
'''

input_dir = '.\Data'
output_dir = '.\Results'

'''
 Get the user-inputs for classifying image-set
'''
def get_user_input():
    #Input - Face/Label/Text
    print("Select image detection property")
    print(" 1. Image classification - Label-Detection")
    print(" 2. Image classification - Face-Detection")
    print(" 3. Image classification - Text-Detection")

    input_value = input("Enter choice 1-3 from above: ")
    if (input_value.isdigit()):
        input_choice = int(input_value)
        if input_choice == 1:
           print("Doing Label-Detection")
        elif input_choice == 2:
           print("Doing Face-Detection")
        elif input_choice == 3:
           print("Doing Text-Detection")
        else:
           print("Invalid Integer Input - Exiting now")
           sys.exit()
    else:
        print("Invalid Input - Exiting now")
        sys.exit()
    return input_choice

'''
 Get the user mode for classifying image-set
 input_mode 2 for Speed Measurements. Ensure Data already exists in AWS bucket
'''
def get_user_mode():
    #Upload - Yes or No
    print("Select image detection mode")
    print(" 1. Upload And Detect - Classic-mode")
    print(" 2. Detect Only (Speed measurements) - Performance-mode")
    input_value = input("Enter mode 1-2 from above: ")
    if (input_value.isdigit()):
        input_mode = int(input_value)
        if input_mode == 1:
           print("Upload and Detect")
        elif input_mode == 2:
           print("Detect")
        else:
           print("Invalid Integer Input - Exiting now")
           sys.exit()
    else:
        print("Invalid Input - Exiting now")
        sys.exit()
    return input_mode

# Results directory and file-names
result_labels_file = os.path.join(output_dir, 'aws_labels_direct.csv')
result_faces_file = os.path.join(output_dir, 'aws_faces_direct.csv')
result_text_file = os.path.join(output_dir, 'aws_text_direct.csv')

fo_labels = open(result_labels_file, "a")
fo_faces = open(result_faces_file, "a")
fo_text = open(result_text_file, "a")

choice = get_user_input()
mode = get_user_mode()

fo_labels.write ("filename" + "," + "class" + "," + "tag1:score1" + "," + "tag2:score2" + "," + "tag3:score3" + "," + "tag4:score4" + "," + "tag5:score5" + "\n")
fo_faces.write ("filename" + "," + "face_present" + "," + "face_detected1" + "score1" + "face_detected2" + "score2" + "face_detected3" + "score3" + "\n")
fo_text.write ("filename" + "," + "extracted_text" + "," + "word_label" + "," + "similarity" + "\n")

'''
  Get the directory/files recursively within a directory and class for label
  detection algorithm
'''
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            # The first directory is used for class extraction
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

# Source: https://stackoverflow.com/a/2077906
def replace_whitespace(string):
    return re.sub(r'\s+', ' ', string).strip()

input_files = getListOfFiles(input_dir)

success_count = 0
# Start time for batch processing
start_time = time.time()
for filename in input_files:
    if os.path.isfile(filename):
       #print(filename)

       bucket_filename = filename;    

       # AWS sets the MinConfidenceScore to 55%
       # Hence if output is < 55%, we will not get any results here
       client=boto3.client('rekognition')

       if choice == 1:
          if mode == 1:
             with open(bucket_filename, 'rb') as image:
                 response = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=5)
                 
          fo_labels.write(filename + ",")
          count = 0
          for label in response['Labels']:
             label_conf_score = float(str(label['Confidence']))
             if label_conf_score > 0:
                count = 1
                fo_labels.write (label['Name'] + ":" + "{:.5f}".format(label['Confidence']/100) + ",")
          fo_labels.write("\n")

       if choice == 2:
       # AWS gets the first 100 faces
          if mode == 1:
             with open(bucket_filename, 'rb') as image:
             #s3.upload_file(filename, bucket_name, bucket_filename)
                 response = client.detect_faces(Image={'Bytes': image.read()})

          print('Detected faces in ' + filename)
          #fo_faces.write(filename + ",")
          index_faces = 0
          for face in response['FaceDetails']:
             face_conf_score = float(str(face['Confidence']))
             index_faces = index_faces + 1
             if (index_faces > 3):
                 break
             
             if (index_faces > 1):
                 fo_faces.write (",")
             if face_conf_score > 0:
                fo_faces.write ("True" + "," + "{:.5f}".format(face['Confidence']/100))
             else:
                fo_faces.write ("True" + "," + "{:.5f}".format(face['Confidence']/100))
             
          if index_faces == 0:
             fo_faces.write ("False")
             
          count = 1
          fo_faces.write("\n")

       if choice == 3:
       # AWS gets the first 100 faces
          if mode == 1:
             with open(bucket_filename, 'rb') as image:
             #s3.upload_file(filename, bucket_name, bucket_filename)
                 response = client.detect_text(Image={'Bytes': image.read()})
             
          fo_text.write(filename + ",")
          index_text = 0
          descriptions = ''
          for text in response['TextDetections']:
             #ignore lines, just get words detected
             text_type = str(text['Type'])
             if text_type == 'WORD':
                text_conf_score = float(str(text['Confidence']))
                index_text = index_text + 1
                count = 1

                if text_conf_score > 0:
                   descriptions = descriptions + ':' + replace_whitespace(text['DetectedText'])

          descriptions = descriptions.lower().split(':')  # Convert to lowercase list
          descriptions = list(set(descriptions))          # Remove duplicates
          descriptions.sort()

          if index_text >= 1:
             out_str = ""
             for word in descriptions:
                 out_str = out_str + word + ":"
             
             fo_text.write (out_str)
          fo_text.write("\n")

    if count == 1:
       success_count = success_count + 1

    if success_count == 500:
       break

    count = 0
# End time for batch processing
end_time = time.time()
print("Successfully classified: " + str(success_count) + " images")
print('Time taken: {} seconds'.format(end_time - start_time))

# Close the result files after all is done
fo_labels.close()
fo_faces.close()
fo_text.close()
print("************DONE*************************")
