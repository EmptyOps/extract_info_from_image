#!/usr/bin/python
from PIL import Image
import os, sys


#use absolute paths
ABS_PATh = os.path.dirname(os.path.abspath(__file__)) + "/"

"""
import tensorflow as tf
flags = tf.app.flags
flags.DEFINE_string("dir_to_process", "", "dir_to_process")
flags.DEFINE_string("crop_top", "", "crop_top")
flags.DEFINE_string("crop_left", "", "crop_top")
flags.DEFINE_string("crop_width", "", "crop_top")
flags.DEFINE_string("crop_height", "", "crop_top")
FLAGS = flags.FLAGS
"""
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='a crop utility')

parser.add_argument('--dir_to_process', type=str, nargs='?',
                    help='dir_to_process')
parser.add_argument('--crop_top', type=str, nargs='?',
                    help='crop_top')
parser.add_argument('--crop_left', type=str, nargs='?',
                    help='crop_left')
parser.add_argument('--crop_width', type=str, nargs='?',
                    help='crop_width')
parser.add_argument('--crop_height', type=str, nargs='?',
                    help='crop_height')
                    
FLAGS = parser.parse_args()
print(FLAGS)


if FLAGS.dir_to_process == "":
    paths = []  #specify static here
else:
    paths = [ FLAGS.dir_to_process+"/" ]

def resize( path ):
    items = os.listdir( path )
    for item in items:
        print(item)
        if item == '.DS_Store':
            continue


        print('here 1')
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imCrped = im.crop((int(FLAGS.crop_left), int(FLAGS.crop_top), int(FLAGS.crop_left)+int(FLAGS.crop_width), int(FLAGS.crop_top)+int(FLAGS.crop_height)))

            #remove original 
            os.remove(path+item)

            imCrped.save(f + e)


for path in paths:
    resize( path )