import sys
import pandas as pd
import numpy as np
import csv
import re
import os

inp_path = '/home/avikbasu/WORK/Economics_of_Innovation/TimeWise'
out_path = '/home/avikbasu/WORK/Economics_of_Innovation/ResearchFall16/doc_IDs'

def map_doc_id(input_filename, output_filename):
    #df = pd.read_csv(os.path.join(dir_path, input_filename),
    #                error_bad_lines=False, warn_bad_lines=False)
    weblink_patt = re.compile(r'\d+$')
    #print len(df)
    #raw_input()

    with open(os.path.join(out_path, output_filename),'w') as out_file:
        with open(os.path.join(inp_path,input_filename),'r') as f:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                m = weblink_patt.search(row[15])
                print i
                i += 1
                if m:
                    out_file.write(m.group(0) + '\n')
                else:
                    out_file.write("None" + '\n')


if __name__ == '__main__':
    name = sys.argv[1]
    map_doc_id(name, name.split('.')[0] + '_docID.txt')
