#!/usr/bin/python3.8
#-*- coding: utf-8 -*-

'''
* The program is aim to parse the fixed-width-file (with provided spec file)and 
  generate a delimited file (CSV file now only)

* The spec file is supposed to meet below requirement: 
   1) Located in folder /data.
   2) It is a json file with extention '.json'.
   3) It should contains ColumnNames as a column list.
   4) It should contains Offsets as a width list.
   5) Number of Columnnames should equals to number of Offsets.
   6) It should contains FixedWidthEncoding value is 'windows-1252'.
   7) It should contains IncludeHeader value only 'True' or 'False' are accepted.
   8) It should contains DelimitedEncoding value is 'utf-8'.

* The output CSV file should meet below requirements:
   1) It should be stored with encoding 'utf-8'

* Rejected records stores in folder '/rejected/'.

'''


import argparse
import time
from datetime import date, timedelta, datetime
import os
import json
import csv

# Read from fixed width string and separate into columns
def slices(s, lengths):
    position = 0
    for length in lengths:
        yield s[position:position + length]
        position += length


def main(spec_filename:str, fixed_width_filename:str):

    start_time = time.time()
    print ("Start at {}".format(datetime.fromtimestamp(start_time)))

    if (not spec_filename.endswith('.json')):
        print ('[ERROR]: please offer a Json File name ends with .json')
        return 1
    elif (not fixed_width_filename.endswith('.FWF')):
        print ('[ERROR]: please offer a Fixed Width File name ends with .FWF')
        return 1    
    else:
        dest_filename = fixed_width_filename[:-4] + '.csv'

    # open spec file
    file_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/data/'
    try:
        with open(file_path + spec_filename, 'r') as spec_file:
            spec = json.load(spec_file)
            print ('[INFO]: Open the spec file successfully.')

            # read spec.json, validate and read offsets     
            column_names = spec.get('ColumnNames')
            offsets = spec.get('Offsets')
            offsets = [int(i) for i in offsets]  # string -> int
            fixed_width_encoding = spec.get('FixedWidthEncoding')
            include_header = spec.get('IncludeHeader')
            delimited_encoding = spec.get('DelimitedEncoding')

            print ('[INFO]: Close the spec file successfully.')
    except IOError as err:
        print ('[ERROR]: Fail to open the spec file. ' + str(err))
        return 1   

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

    lines = []
    rejected_lines = []
    parsed_count = 0
    saved_count = 0
    rejected_count = 0
    # open FWF file
    try:
        with open(file_path + fixed_width_filename, 'rb') as fixed_width_file:
            print ('[INFO]: Open the fixed width file successfully.')
            # read file
            for line in fixed_width_file:
                # decode windows-1252 to unicode
                line = line.decode()
                data = []
                position = 0
                line_lenght = len(line)-1

                for length in offsets:
                    if (position < line_lenght):
                        data.append(line[position:position + length].strip())
                    position += length

                if (position==line_lenght):
                    # save to csv file without import csv
                    lines.append(data)
                    parsed_count += 1
                else:
                    line = line.encode(fixed_width_encoding)
                    rejected_lines.append(line)
                    rejected_count += 1
                
            print ('[INFO]: Close the fixed width file successfully.')
    except IOError as err:
        print ('[ERROR]: Fail to open the fixed width file. ' + str(err))
        return 1

    if (parsed_count > 0):
        # open csv file
        try:
            with open(file_path + dest_filename, 'w', encoding='utf-8', newline='') as csv_file:
                print ('[INFO]: Open the csv file successfully.')
                csv_writer = csv.writer(csv_file, dialect='unix')
                for line in lines:
                    csv_writer.writerow(line)
                    saved_count += 1
                print ('[INFO]: Close the CSV file successfully.')
                print (f'[INFO]: Successfully saved lines: {saved_count}')
                print (f'[INFO]: Successfully parsed the fixed-width-file to CSV file: {dest_filename} .')
        except IOError as err:
            print ('[ERROR]: Fail to open the csv file. ' + str(err))
            return 1
    else:
        print ('[INFO]: No recorde parsed.')

    if (rejected_count > 0):
        file_path = file_path + 'rejected/'
        try:
            with open(file_path + fixed_width_filename, 'wb+' ) as rejected_file:
                print ('[INFO]: Open the rejected file successfully.')
            
                for rejected_line in rejected_lines:
                    rejected_file.write(rejected_line)
                print (f'[INFO]: Close the rejected file successfully.')
        except IOError as err:
            print ('[ERROR]: Fail to open the reject file. ' + str(err))
            return 1                                    
        print (f'[INFO]: Rejected lines: {rejected_count}')
        print (f'[INFO]: Rejected to file: /rejected/{dest_filename}')

parser = argparse.ArgumentParser()
parser.add_argument("-s", dest="SpecFile", required=True, help="Spec file name", type=str)
parser.add_argument("-f", dest="FixedWidthFile", required=True, help="Fixed width file name", type=str)
args = parser.parse_args()

main(args.SpecFile, args.FixedWidthFile)