import io
from pathlib import Path
import pandas as pd
import numpy as np
import time
import nltk

nltk.download('wordnet')


class Labeler:
    def __init__(self, input_dir):

        self.input_dir = input_dir
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        target_path = Path('../azure_output/labels.hd5')

        if target_path.is_file():
            self.data = pd.read_hdf(target_path)
        else:
            self.data = pd.DataFrame(columns=['path', 'class'])
            self._create_dataset()

    def _extract_label(self, path):
        raw_label = path.parts[-2].split('_')[0]
        return self.lemmatizer.lemmatize(raw_label)

    def _create_dataset(self):
        paths = self.input_dir.rglob('*.jpg')
        for p in paths:
            label = self._extract_label(p)
            row = pd.DataFrame([[p, label]], columns=['path', 'class'])
            self.data = self.data.append(row, ignore_index=True)
            print(row)

    def _add_tags(self):
        self.data['tags'] = self.data.apply()

