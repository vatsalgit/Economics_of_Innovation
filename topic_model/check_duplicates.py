import pandas as pd
import os
import re
import csv

def check_duplicates_doc_id():
    # CHECKS ONLY THE DOC IDS FOR DUPLICATES (FROM DOC IDS TXT FILES)
    inp_path = '/home/avikbasu/WORK/Economics_of_Innovation/ResearchFall16/paper_IDs'
    out_path = '/home/avikbasu/WORK/Economics_of_Innovation/Aparna'
    for root, dirs, files in os.walk(inp_path):
        for name in files:
            print "check file: ",name
            all_ids = {}
            output_filename = name.split('_')[0]+"_duplicates.txt"
            with open(os.path.join(out_path, output_filename),'w') as out_file:
                with open(os.path.join(inp_path, name),'r') as in_file:
                    for line in in_file.readlines():
                        line = line.strip()
                        if line not in all_ids:
                            all_ids[line]=1
                        else:
                            print "Found duplicate!"
                            out_file.write(line+'\n')

def check_duplicates_csv():
    # CHECKS IDS WITH ABSTRACTS TO IDENTIFY UNIQUE DUPLICATES (FROM CSV FILES)
    inp_path = '/home/avikbasu/WORK/Economics_of_Innovation/TimeWise'
    out_path = '/home/avikbasu/WORK/Economics_of_Innovation/Aparna/IDs_w_abstracts'
    for root, dirs, files in os.walk(inp_path):
        for name in files:
            print "Checking file: ",name
            all_ids = {}
            weblink_patt = re.compile(r'\d+$')
            output_filename = name.split('.')[0]+"_duplicates.csv"
            with open(os.path.join(out_path, output_filename),'w') as out_file:
                with open(os.path.join(inp_path,name),'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        m = weblink_patt.search(row[15])
                        if m:
                            id = m.group(0)
                            abstract = str(row[10]).replace(',','_')
                            if id not in all_ids:
                                all_ids[id]=abstract
                            else:
                                if abstract==all_ids[id]:
                                    print "Found duplicate!"
                                    out_file.write(id + ',Full_dupl' + ',' + abstract + '\n')
                                else:
                                    print "Found ID duplicate only!"
                                    out_file.write(id + ',ID_dupl' + ',' + abstract + '\n')

def number_of_duplicates():
    inp_path = '/home/avikbasu/WORK/Economics_of_Innovation/Aparna/IDs_w_abstracts'
    out_path = '/home/avikbasu/WORK/Economics_of_Innovation/Aparna'
    output_filename = 'number_of_duplicates.txt'
    with open(os.path.join(out_path, output_filename),'w') as out_file:
        for root, dirs, files in os.walk(inp_path):
            for name in files:
                print "Checking file: ",name
                with open(os.path.join(inp_path,name),'r') as f:
                    year = name.split('_')[0]
                    out_file.write("Year "+year+" : "+str(len(f.readlines()))+'\n')

def remove_duplicates():
    path = '/home/avikbasu/WORK/Economics_of_Innovation/Removed_duplicates_timewise'
    heads = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
    for root, dirs, files in os.walk(path):
        for name in files:
            print "Checking file: ",name
            toclean = pd.read_csv(os.path.join(path, name),names=heads)
            toclean.drop_duplicates(['P'],inplace=True)
            toclean.to_csv(os.path.join(path, name),index=False)

if __name__ == '__main__':
    #check_duplicates_doc_id()
    #check_duplicates_csv()
    #number_of_duplicates()
    remove_duplicates()
