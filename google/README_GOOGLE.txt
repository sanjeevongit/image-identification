README Notes for executing and analysing Google Cloud Vision 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Running Environment: Windows 10, Python 3.6.8

Python package requirements:
- pandas
- google-cloud-vision
- nltk
- tqdm

============================================================

Setup of Google API for Windows
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
1. Follow the tutorial at https://cloud.google.com/vision/docs/quickstart
    i.e. Create a project on Google Cloud Platform, and enable the Google
         cloud vision API for that project.

2. Get the json credentials for your Google Cloud account following the
   instructions at https://console.cloud.google.com/apis/credentials/serviceaccountkey.
   Put that json file in the google folder that you're going to run the code.
   Rename that file as 'google_cloud_authentication.json'. If you didn't follow 
   these last 2 steps, then edit the line of code that says
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'google_cloud_authentication.json')
   and change it so that the path points to where your json credential file is.

3. Gather the data you want to run through the code. Our data file structure was:
- data
    - Faces
        - image_0001.jpg
        ...
    - FERET
        - 100Mammals_n01861778
            - 0.jpg
            ...
    - ImageNet
        - bicycle_n02834778
            - 0.jpg
            ...
        - birds_n01604330
            - 0.jpg
            ...
        - dog_n02084071
            - 0.jpg
            ...
        ...
    - SVT
        -img 
            -00_00.jpg
            ...
        svt_labels.csv
If you arrange your data files in the same way, you shouldn't need to change
the code. Otherwise, you'll have to change the data path in the code. You may
run into errors when running the text_extractor.py if you don't download the full
dataset beforehand because it will look for images that aren't in the data folder.

4. Create an empty output folder

5. Run each file in the google folder

6. Examine results in the output folder.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Overall, the folder structure should be:
- google
    - face_detector.py
    - google_cloud_authentication.json
    - labeler.py
    - text_extractor.py
- data (see above for the structure of the data folder)
- output
- other folders for aws/azure
