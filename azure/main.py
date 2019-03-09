import json
import label
from azure.cognitiveservices.vision.computervision import ComputerVisionAPI
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from pprint import pprint
from pathlib import Path

# Get region and key from environment variables
# Set credentials
# credentials = CognitiveServicesCredentials(key)


def create_client():
    with open('config.json') as cf:
        config = json.load(cf)
    pprint(config)
    region = config['AZURE']['ACCOUNT_REGION']
    key = config['AZURE']['ACCOUNT_KEY']
    # Set credentials
    credentials = CognitiveServicesCredentials(key)

    # Create client
    return ComputerVisionAPI(region, credentials)


# client = ComputerVisionAPI(region, credentials)

if __name__ == '__main__':
    client = create_client()
    label_path = Path("../data/ImageNet")

    l = label.Labeler(label_path)
    print (l.data)

# execute only if run as the entry point into the program
