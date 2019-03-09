import io
import os
import pandas as pd
import re
import time
import nltk
import pprint


class Labeler:
    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self._create_dataset()

    def _extract_label(self, path):
        m = re.search(r'(\\)(.+)(_)', path)
        return m.group(2)

    def _create_dataset(self):
        self.data = pd.DataFrame(columns=['path', 'class'])
        list(self.input_dir.rglob('*.jpg', '.jpeg', '.png'))
        # for path, directories, files in os.walk(self.input_dir):
        #     for file in files:
        #         filename, file_extension = os.path.splitext(file)
        #         if file_extension.strip().lower() == '.jpg':
        #             raw_label = self._extract_label(path)
        #             label = self.lemmatizer.lemmatize(raw_label)
        #             row = pd.DataFrame([[os.path.join(path, file), label]], columns=['path', 'class'])
        #             self.data = self.data.append(row, ignore_index=True)

# tags = pd.DataFrame(columns=['tags', 'scores', 'success'])
# start_time = time.time()
