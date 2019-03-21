import nltk
import os
import sys
nltk.download('wordnet')

lemmatizer = nltk.stem.WordNetLemmatizer()

def get_lemmatize_class(classname):
    lmtz_label = lemmatizer.lemmatize(classname)
    return lmtz_label
    
input_dir = '.\Results'
input_file = os.path.join(input_dir, 'aws_labels.csv')

fo_label = open(input_file, 'r')

count = 0
score = float(0)
total_count = 0

for line in fo_label:
    #print(line)
    values = line.split(',')
    image_class = get_lemmatize_class(values[1])
    labels = values[1].split(':')

    for label in labels:
        print(label)
    print("File text :" + values[1] + " Lemmatize image class :" + image_class)
    i = 0
    #print("Values are " + str(len(values)))
    for column_index in range(len(values)):
        if ((column_index == 0) or (column_index == 1)):
           continue
    
        # Empty or new line colums. Sometimes < 5 labels
        if values[column_index] == " " or values[column_index] == "\n" or values[column_index] == "":
           continue

        match_text = values[column_index].split(':')
        if image_class.lower() == match_text[0].lower():
           count = count + 1
           print("Match " + image_class + " With " + match_text[0] + " Score " + match_text[1])
           score = score + float(match_text[1])
        #else:
           #print("No Match " + image_class + " With " + match_text[0] + " Score " + match_text[1])
           #print()
           
    total_count = total_count + 1

print("Total Matched Conf Score : ", score)
print("Total Match Count: ", count)
print("Total Count: ", total_count-1)
print("Avg Conf_Score   : ", (score/(total_count-1)))
fo_label.close()
