import json
import label
from azure.cognitiveservices.vision.computervision import ComputerVisionAPI
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from pprint import pprint
from pathlib import Path
import numpy as np
import pandas as pd

import io


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


if __name__ == '__main__':
    label_path = Path("../data/ImageNet")
    l = label.Labeler(label_path)

    client = create_client()
    n = 5
    f = l.data.head(n)
    f.apply()
    full_labels = f.apply()

    open(Path(l.data['path'][1]), "rb")
    # d = client.tag_image_in_stream(sample)


# execute only if run as the entry point into the program
