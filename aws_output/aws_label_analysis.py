import os
import sys

   
input_dir = '.\Results'
#input_file = os.path.join(input_dir, 'aws_labels_synonyms.csv')
input_file = os.path.join(input_dir, 'aws_labels.csv')

fo_label = open(input_file, 'r')

count = 0
score = float(0)
debug_count = 0


#Process line output like this
#.\Data\ImageNet\jet_n03335030\0.jpg,jet:aircraft,Airplane:0.9930,Transportation:0.99309,Vehicle:0.99309,Aircraft:0.99309,Warplane:0.94212
# values are comma separated
# labels are colon separated from 2nd value above. jet:aircraft.
# works for 1 label or multiple labels
#

for line in fo_label:
    values = line.split(',')
    labels = values[1].split(':')
    column_index = 0
    #print("Values are " + str(len(values)))
    for column_index in range(len(values)):
        if ((column_index == 0) or (column_index == 1)):
           continue

        # Empty or new line colums. Sometimes < 5 labels
        if values[column_index] == " " or values[column_index] == "\n" or values[column_index] == "":
           continue

        for label in labels:
            image_class = label
            match_text = values[column_index].split(':')
            if image_class.lower() == match_text[0].lower():
               count = count + 1
               print("Match " + image_class + " With " + match_text[0] + " Score " + match_text[1])
               score = score + float(match_text[1])

    #Stop script early change debug_count to 10 or less
    debug_count = debug_count + 1
    if debug_count == 500:
       break

print("Total Conf Score : ", score)
print("Total Match Count: ", count)
print("Avg Conf_Score   : ", (score/count))
fo_label.close()
