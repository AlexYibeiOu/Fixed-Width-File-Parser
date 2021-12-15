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
        print (dest_filename)

    # open spec file
    file_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/data/'
    try:
        with open(file_path + spec_filename, 'r') as spec_file:
            spec = json.load(spec_file)
            print ('[INFO]: Open spec file success.')
    except IOError as err:
        print ('[ERROR]: Fail to open spec file. ' + str(err))
        return 1   

    # read spec.json, validate and read offsets     
    column_names = spec.get('ColumnNames')
    offsets = spec.get('Offsets')
    offsets = [int(i) for i in offsets]  # string -> int
    fixed_width_encoding = spec.get('FixedWidthEncoding')
    include_header = spec.get('IncludeHeader')
    delimited_encoding = spec.get('DelimitedEncoding')
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
        print ('[INFO]: Validation of spec file success.')

    # open FWF file
    lines = []
    try:
        with open(file_path + fixed_width_filename, 'rb') as fixed_width_file:

            # read file
            for line in fixed_width_file:
                # decode windows-1252 to unicode
                line = line.decode('windows-1252')
                # encode unicode to utf-8
                #line = line.encode('utf-8')
                #print(line)

                data = []
                position = 0
                for length in offsets:
                    data.append(line[position:position + length].strip())
                    position += length
                print (data)

                # save to csv file without import csv
                lines.append(data)

            print ('Parse to CSV successfully.')
    except IOError as err:
        print ('[ERROR]: Fail to open fixed width file. ' + str(err))
        return 1

    # open csv file
    try:
        with open(file_path + dest_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='unix')
            for line in lines:
                csv_writer.writerow(line)
    except IOError as err:
        print ('[ERROR]: Fail to open csv file. ' + str(err))
        return 1

    csv_file.close()
    print ('[INFO]: Close csv file successfully.')

    # close file
    spec_file.close()
    print ('[INFO]: Close spec file successfully.')

    fixed_width_file.close()
    print ('[INFO]: Close fixed width file successfully.')

parser = argparse.ArgumentParser()
parser.add_argument("-s", dest="SpecFile", required=True, help="Spec file name", type=str)
parser.add_argument("-f", dest="FixedWidthFile", required=True, help="Fixed width file name", type=str)
args = parser.parse_args()

main(args.SpecFile, args.FixedWidthFile)