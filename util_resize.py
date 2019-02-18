#!/usr/bin/python
from PIL import Image
import os, sys

import tensorflow as tf

#use absolute paths
ABS_PATh = os.path.dirname(os.path.abspath(__file__)) + "/"


flags = tf.app.flags
flags.DEFINE_string("dir_to_process", "", "dir_to_process")
flags.DEFINE_string("resize_width", "", "resize_height")
flags.DEFINE_string("resize_height", "", "resize_height")
FLAGS = flags.FLAGS

if FLAGS.dir_to_process == "":
    paths = []  #specify static here
else:
    paths = [ FLAGS.dir_to_process+"/" ]

def resize( path ):
    for item in dirs:
        print(item)
        if item == '.DS_Store':
            continue


        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize(( int(FLAGS.resize_width), int(FLAGS.resize_height) ), Image.ANTIALIAS)

            #remove original 
            os.remove(path+item)

            imResize.save(f + '.jpg', 'JPEG', quality=90)


for path in paths:
    dirs = os.listdir( path )
    resize( path )