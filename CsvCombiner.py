import os
import pandas as pd
import csv
import numpy as np

def Save(row_list , filename="Combined"): #takes list of emails and file name to save on to
    filename = filename+'.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in row_list:
            writer.writerow([i])

names = os.listdir()

names = [i for i in names if '.csv' in i]
if(len(names)>1):

    fin = []
    for i in names:
        with open(i) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                fin.extend(row)

    #emails = {'Email' : fin }
    Save(fin)
    print(fin[0:20])
    print('Done...')
else:
    print('No files to combine')
    
