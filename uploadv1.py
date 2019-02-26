import sys
import os
import boto3

bucket_name = 'coen241-istore'
s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name)
print('Creating Amazon s3 bucket: ' + bucket_name)
# upload a file to the s3 bucket

path = '.\Photos'

if len(sys.argv) == 2:
    path = sys.argv[1]

files = os.listdir(path)
for name in files:
    print(name)

    full_path = os.path.join(path, name)
    print(full_path)

    if os.path.isfile(full_path):
#       print(full_path)

       s3.upload_file(full_path, bucket_name, name)

       client=boto3.client('rekognition')
       response = client.detect_labels(Image={'S3Object':{'Bucket':bucket_name,'Name':name}})
       print('Detected labels for ' + name)

       for label in response['Labels']:
          conf_score = float(str(label['Confidence']))
#          print (conf_score)
          if conf_score > 90:
             print (label['Name'] + ' : ' + str(label['Confidence']))

print("*************************************")


