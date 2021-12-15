import argparse
import time
import os
import json
import random
from datetime import date, timedelta, datetime

def main(json_filename:str, amount:int):

    start_time = time.time()
    print ("Start at {}".format(datetime.fromtimestamp(start_time)))

    if (not json_filename.endswith('.json')):
        print ('[ERROR]: please offer a Json File name ends with .json')
        return 1
    else:
        dest_filename = json_filename[:-4] + str(datetime.fromtimestamp(start_time)).replace(' ','.').replace(':','.') + '.FWF'
        print (dest_filename)

    # open spec.json
    file_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/data/' 
    try:
        with open(file_path + json_filename, 'r') as spec_file:
            spec = json.load(spec_file)
            print ('[INFO]: Open spec file success.')
    except IOError as err:
        print ('[ERROR]: Fail to open spec file. ' + str(err))
        return 1    

    # read spec.json, validate and read offsets     
    column_names = spec.get('ColumnNames')
    offsets = spec.get('Offsets')
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

    # open destination file
    dest_file = open(file_path + dest_filename, 'wb')

    # add header
    line = ''
    for i in zip(column_names, offsets):
        line += ('{:<{fixed_width}}'.format(i[0], fixed_width=i[1]))
    line += '\n'
    # encode to windows-1252
    line_windows1252 = line.encode('windows-1252')
    # save to file
    dest_file.write(line_windows1252)

    for n in range(1, amount+1): 
        # random generate data
        data = []
        int_line = [1,2]
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

        # add end of line
        if ( n < amount):
            line += '\n'

        # encode to windows-1252
        line_windows1252 = line.encode('windows-1252')

        # save to file
        dest_file.write(line_windows1252)

        # print screen information
        if (n % 20000 == 0):
            print ("[INFO]: {} lines are generated. Used {} seconds.".format(n, int(time.time()-start_time)))

    # close file
    dest_file.close()
    print ('[INFO]: Close destination file successfully.')
    spec_file.close()
    print ('[INFO]: Close spec file successfully.')

    print ("[INFO]: {} lines are generated. Used {} seconds.".format(amount, int(time.time()-start_time)))
    print ('[INFO]: Fixed width file generated successfully.')    

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="InputFile", required=True, help="Spec file name", type=str)
parser.add_argument("-n", dest="Number", required=False, help="Amount of lines to be generated, defaul is 100.", type=int, default=100)
args = parser.parse_args()

main(args.InputFile, args.Number)
