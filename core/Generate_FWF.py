#!/usr/bin/python3.8

'''
* This program is aim to generate a fixed width file, using the provided spec.
 
* The width is the offset provided in the spec file represent the length of each field.

* The spec file is supposed to meet below requirement: 
   1) Located in folder /data
   2) It is a json file with extention .json
   3) It should contains ColumnNames as a column list
   4) It should contains Offsets as a width list
   5) Number of Columnnames should equals to number of Offsets
   6) It should contains FixedWidthEncoding value is 'windows-1252'
   7) It should contains IncludeHeader value only 'True' or 'False' are accepted
   8) It should contains DelimitedEncoding value is 'utf-8'

* The generated fixed-width-file is supposed to:
   1) Located in folder /data
   2) File name start with the same of spec file and appended daytime
   3) File extention is .FWF
   4) Randomly generate integer/string in the file encoded with 'windows-1252'.
   6) Which colum(s) is/are integer specify in variable int_line (hardcoded now)

'''

import argparse
import time
import os
import json
import random
from datetime import date, timedelta, datetime

def main(json_filename:str, amount:int):

    start_time = time.time()
    print ("Start at {}".format(datetime.fromtimestamp(start_time)))
    int_line = [0,5]

    if (not json_filename.endswith('.json')):
        print ('[ERROR]: Please offer a Json File name ends with .json')
        return 1
    else:
        dest_filename = json_filename[:-4] + str(datetime.fromtimestamp(start_time)).replace(' ','.').replace(':','.') + '.FWF'

    # open spec.json
    file_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/data/' 
    try:
        with open(file_path + json_filename, 'r') as spec_file:
            spec = json.load(spec_file)
            print ('[INFO]: Open the spec file successfully.')

            # read spec.json
            column_names = spec.get('ColumnNames')
            offsets = spec.get('Offsets')
            fixed_width_encoding = spec.get('FixedWidthEncoding')
            include_header = spec.get('IncludeHeader')
            delimited_encoding = spec.get('DelimitedEncoding')

            print ('[INFO]: Close the spec file successfully.')
    except IOError as err:
        print ('[ERROR]: Fail to open the spec file. ' + str(err))
        return 1    

    # validate and read offsets
    if (column_names == 'None'):
        print("[ERROR]: Can't find ColumnNames in spec file.")
        return 1
    elif (offsets == 'None'):
        print ("[ERROR]: Can't find Offsets in spec file.")
        return 1
    elif (fixed_width_encoding == 'None'):
        print ("[ERROR]: Can't find fixed_width_encoding in spec file.")
        return 1
    elif (include_header == 'None'):
        print ("[ERROR]: Can't find include_header in spec file.")
        return 1
    elif (delimited_encoding == 'None'):
        print ("[ERROR]: Can't find delimited_encoding in spec file.")
        return 1
    elif (len(column_names) != len(offsets)):
        print ("[ERROR]: Number of ColumnNames and Offsets are different in spec file!")
        return 1
    elif (fixed_width_encoding!='windows-1252'):
        print ("[ERROR]: FixedWidthEncoding value is not windows-1252.")
        return 1
    elif (include_header != 'True' and include_header != 'False'):
        print ('[ERROR]: IncludeHeader value is not correct in spec file.')
        return 1
    elif (delimited_encoding!='utf-8'):
        print ("[ERROR]: delimited_encoding value is not utf-8.")
        return 1
    else:
        print ('[INFO]: Validation of spec file is successful.')


    try:
        # open destination file
        with open(file_path + dest_filename, 'wb+') as dest_file:
            # add header
            line = ''
            for i in zip(column_names, offsets):
                line += ('{:<{fixed_width}}'.format(i[0], fixed_width=i[1]))
            line += '\n'
            # encode to windows-1252 & save to file
            dest_file.write(line.encode('windows-1252'))
            
            for n in range(1, amount+1): 
                # random generate data
                data = []
                current = 0
                for i in offsets:
                    length = random.randint(1, int(i))
                    if ( current in int_line ):
                        data.append(random.randint(1, 10*length-1))
                    else:
                        data.append(''.join(random.sample(['z','y','x','w','v','u','t','s','r',  
                            'q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a',' '], length)))
                    current += 1

                # generate fixed width line
                line = ''
                for i in zip(data, offsets): 
                    line += ('{:<{fixed_width}}'.format(i[0], fixed_width=i[1]))
                line += '\n'

                # encode to windows-1252 & save to file
                dest_file.write(line.encode(fixed_width_encoding))
                
                # print screen information
                if (n % 20000 == 0):
                    print ("[INFO]: {} lines are generated. Used {} seconds.".format(n, int(time.time()-start_time)))

            print ('[INFO]: Close the destination file successfully.')
    except IOError as err:
        print ('File error:' + str(err))
        return 1   

    print ("[INFO]: Summary - {} lines are generated. Used {} seconds.".format(amount, int(time.time()-start_time)))
    print ('[INFO]: Successfully generate this fixed-width-file. Please copy it!')
    print ('[INFO]: {}'.format(dest_filename))

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="InputFile", required=True, help="Spec file name", type=str)
parser.add_argument("-n", dest="Number", required=False, help="Amount of lines to be generated, defaul is 100.", type=int, default=100)
args = parser.parse_args()

main(args.InputFile, args.Number)