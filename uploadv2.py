import sys
import os
import boto3

bucket_name = 'coen241-istore'
s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name)
print('Creating Amazon s3 bucket: ' + bucket_name)
# upload a file to the s3 bucket

input_dir = '.\Photos'
output_dir = '.\Results'

if len(sys.argv) == 2:
    path = sys.argv[1]

# Get the user-inputs for classifying image-set
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

choice = get_user_input()
# Results directory and file-names
result_labels_file = os.path.join(output_dir, 'aws_labels.csv')
result_faces_file = os.path.join(output_dir, 'aws_faces.csv')
result_text_file = os.path.join(output_dir, 'aws_text.csv')

fo_labels = open(result_labels_file, "a")
fo_faces = open(result_faces_file, "a")
fo_text = open(result_text_file, "a")

input_files = os.listdir(input_dir)

for filename in input_files:
    print(filename)

    dir_filename = os.path.join(input_dir, filename)

    if os.path.isfile(dir_filename):
       print(dir_filename)

       s3.upload_file(dir_filename, bucket_name, filename)

       # AWS sets the MinConfidenceScore to 55%
       # Hence if output is < 55%, we will not get any results here
       client=boto3.client('rekognition')

       if choice == 1:
          response = client.detect_labels(Image={'S3Object':{'Bucket':bucket_name,'Name':filename}}, MaxLabels=5)
          print('Detecting labels for ' + filename)
          fo_labels.write(filename + ",")
          for label in response['Labels']:
             label_conf_score = float(str(label['Confidence']))
             if label_conf_score > 0:
                #print (label['Name'] + ':' + str(label['Confidence']))
                fo_labels.write (label['Name'] + ":" + "{:.2f}".format(label['Confidence']) + "%" + ",")
          fo_labels.write("\n")

       if choice == 2:
       # AWS gets the first 100 faces
          response = client.detect_faces(Image={'S3Object':{'Bucket':bucket_name,'Name':filename}})
          print('Detected faces in ' + filename)
          fo_faces.write(filename + ",")
          index_faces = 0
          for face in response['FaceDetails']:
             face_conf_score = float(str(face['Confidence']))
             index_faces = index_faces + 1
             print (conf_score)
             if face_conf_score > 0:
                #print ('Detected Face:', str(face['Confidence']))
                fo_faces.write ("Face:True" + "," + "{:.2f}".format(face['Confidence']) + "%" + ",")
             else:
                fo_faces.write ("Face:False" + "," + "{:.2f}".format(face['Confidence']) + "%" + ",")
          if index_faces == 0:
             fo_faces.write ("Face:False")
          fo_faces.write("\n")

       if choice == 3:
       # AWS gets the first 100 faces
          response = client.detect_text(Image={'S3Object':{'Bucket':bucket_name,'Name':filename}})
          fo_text.write(filename + ",")
          index_text = 0
          for text in response['TextDetections']:
             text_conf_score = float(str(text['Confidence']))
             index_text = index_text + 1
#             print (conf_score)
             if text_conf_score > 0:
                fo_text.write (text['DetectedText'] + ":" + "{:.2f}".format(text['Confidence']) + "%" + ",")                 
                #print ('Detected Text:' + text['DetectedText'] + ':' + str(text['Confidence']))
          if index_text == 0:
             fo_text.write ("Text:False")
          fo_text.write("\n")

# Close the result files after all is done
fo_labels.close()
fo_faces.close()
fo_text.close()
print("************DONE*************************")
