README Notes for executing and analysing Image Rekognition for AWS 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Running Environment: Windows 8.1, AWS SDK Boto 3, Python 3.7
============================================================

Setup of AWS SDK for Windows
++++++++++++++++++++++++++++
1. First and foremost we need credentials for accessing the AWS cloud
via the Windows environment.

More details here: Please follow step 2. in the below html page.
https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html

2. Create an access key for the user you created in Create an IAM User

More details here: Please follow step 2. in the below html page.
https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html

Create an access key and then download the .csv file. 

3. Go to home directory and create a .aws directory. For Windows this is the
location %HOMEPATH%/.aws

4. In the .aws directory create a file named credentials. Copy the contents
of the .csv file you created above in step 2, into this file.

This is the format of credentials file. Replace your_access_key_id and
your_secret_access_key from the .csv file. Just 3 lines.

[default]
aws_access_key_id = your_access_key_id
aws_secret_access_key = your_secret_access_key

5. In the .aws directory, create a new file named config.
Substitute your desired AWS Region (for example, "us-west-2") for your_aws_region.
Just 2 lines.

[default]
region = your_aws_region

C:\Users\SanjeevKumar\.aws>dir
 Volume in drive C is OS
 Volume Serial Number is 38E2-EB5B

 Directory of C:\Users\SanjeevKumar\.aws

02/02/2019  03:29 AM    <DIR>          .
02/02/2019  03:29 AM    <DIR>          ..
02/02/2019  07:49 PM                29 config
03/13/2019  12:24 AM               117 credentials
               2 File(s)            146 bytes
               2 Dir(s)  749,608,509,440 bytes free

Running the python scripts for uploading images and collecting responses:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1. The scripts needs two folders at the same directory where you will run
the python scripts. Create these folders. Folder "Data" for storing the
image data set. Folder "Results" for storing the results (in .csv format).

2. Running aws_detection.py and aws_detection_direct.py.
 
   Two modes of running:
   1) S3 bucket mode: aws_detection uploads file to S3 bucket and then run image detection on those files
   2) Direct mode: aws_detection_direct uploads file directly from local file system to the Cloud APIs and get
      the response.

3. On running aws_detection.py the Menu will appear which is self explanatory:

   Two choices are asked: 
   1) Choice of Label/Face/Text detection
   2) Image detection mode. Choose "Upload and Detect" when running for 1st time.
   3) Image detection mode. Choose "Detect Only" when Image was already uploaded. This works only after once "Upload and Detect" mode
      was already run once. This was needed when Images are already existing in S3 bucket and we are doing label detection
      on images already in the cloud.

Select image detection property
 1. Image classification - Label-Detection
 2. Image classification - Face-Detection
 3. Image classification - Text-Detection
Enter choice 1-3 from above: 1
Doing Label-Detection
Select image detection mode
 1. Upload And Detect - Classic-mode
 2. Detect Only (Speed measurements) - Performance-mode
Enter mode 1-2 from above: 1

4. Please make sure correct Data exists in the ./Data folder for label/face/text detection to be run on.

5. Once the code is run, it will collect the results in the ./Results folder
  1. Label-Detection generates:  aws_labels.csv
  2. Face-Detection generates:  aws_faces.csv
  3. Text-Detection generates:  aws_text.csv

6. aws_detection_direct directly uploads the image to Cloud API, rather than storing it in S3 bucket. So there is
   only one Image Detection mode which is relavant for it is "Upload and Detect".


Once the code is run, it will collect the results in the ./Results folder
  1. Label-Detection generates:  aws_labels_direct.csv
  2. Face-Detection generates:  aws_faces_direct.csv
  3. Text-Detection generates:  aws_text_direct.csv

   There is functionally no difference in doing step 3 v/s step 6. The results are the same. Step 3 did
   s3 bucket upload. Step 6 did direct upload. This was done for comparing the two modes of operation.
   s3 bucker upload was more faster than direct upload.

Analysing the data: Python scripts for analysing aws_labels.csv and aws_text.csv
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1. Mean Confidence Score for label match

   Run aws_label_analysis_lemmatize in the same directory where aws_labels.csv exists.
   This runs the label analysis generating Mean confidence score based on using synonyms (lemmatize).

2. aws_text.csv was extended/filled for another column named "word label". This was done for each image similarly
   for all the three Cloud Service Providers. These are the labels which are text in human readable form appearing
   in the images. Once this column was filled the file was renamed as "aws_text_similarity.csv".

   Mean Jaccard Similarity for text match.

   Run aws_text_analysis in the same directory where aws_text_similarity.csv exists. This will run the
   mean jaccard similarity algorithm for each file for detected text and labelled words for the image and come
   up with a Jaccard Score. The results are part of aws_text_jaccard.csv file

   