#!/usr/bin/python
import os, sys

from PIL import Image, ImageGrab
from matplotlib import pyplot as plt

import cv2  
import numpy as np  
import math
import json

import tensorflow as tf

#use absolute paths
ABS_PATh = os.path.dirname(os.path.abspath(__file__)) + "/"


flags = tf.app.flags
flags.DEFINE_string("dir_to_process", "", "dir_to_process")
flags.DEFINE_string("rgba_value", "", "rgba_value")
flags.DEFINE_string("rgba_check_range_y", "", "rgba_check_range_y")
flags.DEFINE_integer("rgba_accuracy_threshold", 0, "rgba_accuracy_threshold")
FLAGS = flags.FLAGS

if FLAGS.dir_to_process == "":
    paths = []  #specify static here
else:
    paths = [ FLAGS.dir_to_process+"/" ]


def find_subimage_by_rgba(large_image_path, yArrGlb, rgba_valueArr, rgba_accuracy_threshold):

    assert os.path.isfile(large_image_path)

    img = cv2.imread(large_image_path, cv2.IMREAD_UNCHANGED)
    size_x = img.shape[1] 
    #print( "size_x = " + str(size_x) )
    
    is_start_found = False 
    found_cnt_index = -1
    res = {}
    for xv in range(0, size_x):
        """
        #print(xv)
        print( img[50][508] )
        print( img[50][509] )
        print( img[51][508] )
        print( img[51][509] )
        
        print( img[50][32] )
        print( img[50][33] )
        print( img[51][32] )
        print( img[51][33] )

        print( img[50][986] )
        print( img[50][987] )
        print( img[51][986] )
        print( img[51][987] )

        print("bottom")
        
        print( img[60][508] )
        print( img[60][509] )
        print( img[61][508] )
        print( img[61][509] )
        
        print( img[60][32] )
        print( img[60][33] )
        print( img[61][32] )
        print( img[61][33] )

        print( img[60][986] )
        print( img[60][987] )
        print( img[61][986] )
        print( img[61][987] )
        
        dsfdsdsfdf
        #for yv in range(0, 69):
        #    print( img[yv][xv] )
        
        ys = img[ int(yArr[0]) : int(yArr[1]) + 1 ]
        print( ys.shape )
        print( ys[0][xv] )
        print( ys[1][xv] )
        print( ys[2][xv] )
        print( ys[3][xv] )
        """
        
        #if not( (xv >= 32 and xv <= 33) or (xv >= 508 and xv <= 509) or (xv >= 986 and xv <= 987) or (xv >= 1462 and xv <= 1463) or (xv >= 1940 and xv <= 1941) or (xv >= 3370 and xv <= 3371) ):
        #    continue
        #else:
        #    print("got nwennn")

           
        is_match = False
        sizeyGlb = len(yArrGlb)
        for y_posGlb in range(0, sizeyGlb):
            yArr = yArrGlb[y_posGlb]
            sizey = len(yArr)
            
            for y_pos in range(0, sizey):
                #print(img[ yArr[y_pos] ][xv])
                if abs( img[ yArr[y_pos] ][xv][0] - rgba_valueArr[y_pos][0] ) <= rgba_accuracy_threshold and abs( img[ yArr[y_pos] ][xv][1] - rgba_valueArr[y_pos][1] ) <= rgba_accuracy_threshold and abs( img[ yArr[y_pos] ][xv][2] - rgba_valueArr[y_pos][2] ) <= rgba_accuracy_threshold:
                    is_match = True
                else:
                    is_match = False
                    break
                #elif False and ( img[50][xv][1] >= 30 and img[50][xv][1] <= 60 and img[60][xv][1] >= 30 and img[60][xv][1] <= 60 ) img[y_pos][xv][1] == int( rgba_valueArr[1] ) and img[y_pos][xv][2] == int( rgba_valueArr[2] ):
                #    is_match = True
        
        if is_match:
            if is_start_found == False:
                is_start_found = True
                found_cnt_index = found_cnt_index + 1
                res[found_cnt_index] = []
                
                res[found_cnt_index].append( xv )
        else:
            if is_start_found == True:
                res[found_cnt_index].append( xv - 1 )
                is_start_found = False
   
        #if xv >= 3371:
        #    return res
   
    return res
    
def resize( path, res, FLAGS ):

    yArr = []
    yArr_tmp = FLAGS.rgba_check_range_y.split(',')
    size1 = len(yArr_tmp)
    for idx1 in range(0, size1):
        yArr.append( list( map( int, yArr_tmp[idx1].split('-') ) ) )

    
    rgba_valueArr = []
    rgbaArr_tmp = FLAGS.rgba_value.split(',')
    size1 = len(rgbaArr_tmp)
    for idx1 in range(0, size1):
        rgbaArr_inner_tmp = rgbaArr_tmp[idx1].split('-')
        size2 = len(rgbaArr_inner_tmp)
        inner_arr = []
        for idx2 in range(0, size2):
            inner_arr.append( int(rgbaArr_inner_tmp[idx2]) )
    
        rgba_valueArr.append( inner_arr )
    
    #print( "rgba_valueArr" )
    #print( rgba_valueArr )

    for item in dirs:
        #print(item)
        if item == '.DS_Store':
            continue

        if os.path.isfile(path+item):
            f, e = os.path.splitext(item)

            #
            res[f] = find_subimage_by_rgba( path+item, yArr, rgba_valueArr, FLAGS.rgba_accuracy_threshold )
            #print(res[f])
            #sdfsdfsddf
            
            #
            #res[f] = "x=" + str( x ) + ", y=" + str(y)

    return res
            
            
res = {}            
for path in paths:
    dirs = os.listdir( path )
    res = resize( path, res, FLAGS )
    
#for key in res:
#    print("key = " + key + " len " + str( len(res[key]) ) )
    
#res
print( json.dumps(res) ) 
