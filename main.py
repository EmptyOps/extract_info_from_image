import argparse

import sys, os
import json
from numpy import array
import numpy as np
from glob import glob
import json
import collections


# Instantiate the parser
parser = argparse.ArgumentParser(description='a wrapper to extract desired information from images using tesseract etc libs. Note that its a wrapper to extract texts, similar objects by images and accurate details by matching at pixel level ')

# verbose
parser.add_argument('--verbose', action='store_true',
                    help='A boolean True False')

# 
parser.add_argument('--input_dir', type=str, 
                    help='An input_dir, must be provided')
parser.add_argument('--output_dir', type=str, 
                    help='An output_dir to store original extracted information, must be provided')
                    
# 
parser.add_argument('--crop_x', type=int, nargs='?', const=1, 
                    help='An optional crop x, if not passed than crop will be skipped. Note that original image will be removed from dir')
parser.add_argument('--crop_y', type=int, nargs='?',
                    help='crop y, must be supplied if crop_x is provided')
parser.add_argument('--crop_width', type=int, nargs='?',
                    help='crop width, must pass if crop_x is provided')
parser.add_argument('--crop_height', type=int, nargs='?',
                    help='crop height, must pass if crop_x is provided')

# 
parser.add_argument('--resize_width', type=int, nargs='?',
                    help='An optional resize_width, usefull if you want crop and resize to bigger size to make information easily extractable, if not passed than resize will be skipped. Note that cropped/original image will be removed from dir')
parser.add_argument('--resize_height', type=int, nargs='?',
                    help='must be supplied if resize_width is provided')
                    
# 
parser.add_argument('--python_path', type=str, nargs='?',
                    help='optional, python path for subprocess calling need to be provided in case python is not accessible by simply python3 in your system')
                    
# 
parser.add_argument('--extract_text', action='store_true',
                    help='A boolean True False')
parser.add_argument('--parse_format', type=str,  nargs='?',
                    help='will parse and extracts only the meaningful texts like numbers etc from the extract text output, supported options [\'numbers\']')

parser.add_argument('--object_image', type=str,  nargs='?',
                    help='if provided all matching object locations will be extracted')

parser.add_argument('--rgba_value', type=str,  nargs='?',
                    help='if provided all starting and ending points matching with rgba_value will be returned, it is a convention to easily detect all matching object of particular color only. pass RGB and alpha separated by hyphen \'-\' however alpha is not used so far. For e.g if rgba_check_range_y is of length 3 e.g. 99-101 than rgba_value cuuld be like 0-0-255-0,0-0-255-0,0-0-255-0 ')
parser.add_argument('--rgba_check_range_y', type=str,  nargs='?',
                    help='If provided rgba_value will be checked over horizontal direction where rgba_check_range_y is the verticle area to match upon. rgba_check_range_y expects 2 int values separated by hyphen \'-\' for e.g. 33-43 multiple range also supported separated by comma \',\' for e.g. 33-43,540-550 note that even in case of multiple range the rgba_value and the rgba_accuracy_threshold will be single only which means match will be checked against multiple y ranges ')
parser.add_argument('--rgba_accuracy_threshold', type=int,  nargs='?',
                    help='an interger value in range 0 to 255 for extracting similar match, if ignored or 0 than exact match 100% accuracy will only be considered ')
                    
parser.add_argument('--out_to_csv_file', type=str,  nargs='?',
                    help='if provided output will be writtent to csv(semicolon separated) otherwise to stdout. ')
                    
args = parser.parse_args()
print(args)
    
    
pythonp = "python3"
if args.python_path:
  pythonp = args.python_path
    
dirs = glob( args.input_dir + "/*/" )
if len(dirs) == 0:
    dirs = [ args.input_dir ]
    
#crop images if applicable     
if not args.crop_x == None:

    for dir in dirs:
        actual_dir = os.path.basename( os.path.dirname(dir) )

        command = pythonp + " ./util_crop.py --dir_to_process "+dir+" --crop_left "+str( args.crop_x )+" --crop_top "+str( args.crop_y )+" --crop_width "+str( args.crop_width )+" --crop_height "+str( args.crop_height )+" "
        if args.verbose:
            print("executing crop command... " + command)
            
        res_tmp = os.popen(command).read()

        if args.verbose:
            print(res_tmp)
            
        print("crop done")        
    
    
#resize images if applicable     
if args.resize_width and args.resize_width > 0:

    for dir in dirs:
        actual_dir = os.path.basename( os.path.dirname(dir) )

        command = pythonp + " ./util_resize.py --dir_to_process "+dir+" --resize_width "+str( args.resize_width )+" --resize_height "+str( args.resize_height )+" "
        if args.verbose:
            print("executing resize command... " + command)
            
        res_tmp = os.popen(command).read()

        if args.verbose:
            print(res_tmp)
            
        print("resize done")        

    
#extract the text 
res = {}
if args.extract_text:

    res["text"] = {}
    for dir in dirs:
        actual_dir = os.path.basename( os.path.dirname(dir) )
    
        command = pythonp + " ./ocr-convert-image-to-text/main.py --input_dir "+dir+" --output_dir "+ os.path.join(args.output_dir, actual_dir ) +" "
        if args.verbose:
            print("executing extract command... " + command)
            
        res["text"][actual_dir] = os.popen(command).read()

        if args.verbose:
            print(res["text"][actual_dir])
            
        print("extract text done")        
        
        #extract only the meaningful texts like numbers etc
        if args.parse_format:
            if args.parse_format == 'numbers':
                raise Exception("Not Implemented Error, sorry parse_format with numbers isn't supported yet")    

        
#extract the object location 
if args.object_image:

    res["obj_locations"] = {}
    for dir in dirs:
        actual_dir = os.path.basename( os.path.dirname(dir) )

        command = pythonp + " ./detect_object_locations.py --dir_to_process "+dir+" --object_image "+ args,object_image +" "
        if args.verbose:
            print("executing extract object location command... " + command)
            
        res["obj_locations"][actual_dir] = os.popen(command).read()

        if args.verbose:
            print(res["obj_locations"][actual_dir])
            
        print("extract object location done")    

    
#extract the object locations based on rgba_value
if args.rgba_value:

    res["obj_locations_by_rgba"] = {}
    for dir in dirs:
        actual_dir = os.path.basename( os.path.dirname(dir) )

        command = pythonp + " ./detect_object_locations_based_on_color.py --dir_to_process "+dir+" --rgba_value "+ args.rgba_value +" --rgba_check_range_y "+ args.rgba_check_range_y +" --rgba_accuracy_threshold "+ ( str(0) if args.rgba_accuracy_threshold == None else str(args.rgba_accuracy_threshold) ) +" "
        if args.verbose:
            print("executing extract object location by rgba_value command... " + command)
            
        res["obj_locations_by_rgba"][actual_dir] = os.popen(command).read()

        if args.verbose:
            print(res["obj_locations_by_rgba"][actual_dir])
            
        print("extract object location by rgba_value done")  

        
#out_to_csv_file
if args.out_to_csv_file:

    with open( args.out_to_csv_file, 'wb' ) as file:
    
        for dir in dirs:
            actual_dir = os.path.basename( os.path.dirname(dir) )

            if "text" in res:
                if actual_dir in res["text"]:
                
                    items = os.listdir( dir )
                    for item in items:
                        
                        with open( dir + item, 'r', errors='ignore' ) as myfile:
                            strv = " ; " + myfile.read() + "; " 
                            print( strv )
                        
                            line = "\""+actual_dir+"\";\""+item+"\";\""+ myfile.read() +"\"" 
                            file.write(line.encode())
                            file.write('\n'.encode())
                
            if "object_locations" in res:
                file.write( str( res["object_locations"] ).encode() )
                file.write('\n'.encode())

            if "obj_locations_by_rgba" in res:
                if actual_dir in res["obj_locations_by_rgba"]:
                
                    dictjson = json.loads( res["obj_locations_by_rgba"][actual_dir] )
                    dictjson = collections.OrderedDict(sorted(dictjson.items()))
                    
                    for keyinr in dictjson:
                        line = "\""+actual_dir+"\";\""+keyinr+"\";\""+ json.dumps( dictjson[keyinr], sort_keys=True ) +"\"" 
                        file.write(line.encode())
                        file.write('\n'.encode())
    
else: 
    if "text" in res:
        print(res["text"])
        
    if "object_locations" in res:
        print(res["object_locations"])        

    if "obj_locations_by_rgba" in res:
        print(res["obj_locations_by_rgba"])        
        
    
# some debug 
if args.verbose == True:
    tmp = ''     

    