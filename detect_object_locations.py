#!/usr/bin/python
import os, sys

from PIL import Image, ImageGrab
from matplotlib import pyplot as plt

import cv2  
import numpy as np  

import tensorflow as tf

#use absolute paths
ABS_PATh = os.path.dirname(os.path.abspath(__file__)) + "/"


flags = tf.app.flags
flags.DEFINE_string("dir_to_process", "", "dir_to_process")
flags.DEFINE_string("object_image", "", "object_image")
FLAGS = flags.FLAGS

if FLAGS.dir_to_process == "":
    paths = []  #specify static here
else:
    paths = [ FLAGS.dir_to_process+"/" ]



def iter_rows(pil_image):
    """Yield tuple of pixels for each row in the image.

    From:
    http://stackoverflow.com/a/1625023/1198943

    :param PIL.Image.Image pil_image: Image to read from.

    :return: Yields rows.
    :rtype: tuple
    """
    iterator = zip(*(iter(pil_image.getdata()),) * pil_image.width)
    for row in iterator:
        yield row


def find_subimage(large_image, subimg_path):
    """Find subimg coords in large_image. Strip transparency for simplicity.

    :param PIL.Image.Image large_image: Screen shot to search through.
    :param str subimg_path: Path to subimage file.

    :return: X and Y coordinates of top-left corner of subimage.
    :rtype: tuple
    """
    # Load subimage into memory.
    with Image.open(subimg_path) as rgba, rgba.convert(mode='RGB') as subimg:
        si_pixels = list(subimg.getdata())
        si_width = subimg.width
        si_height = subimg.height
    si_first_row = tuple(si_pixels[:si_width])
    si_first_row_set = set(si_first_row)  # To speed up the search.
    si_first_pixel = si_first_row[0]

    # Look for first row in large_image, then crop and compare pixel arrays.
    for y_pos, row in enumerate(iter_rows(large_image)):
        if si_first_row_set - set(row):
            continue  # Some pixels not found.
        for x_pos in range(large_image.width - si_width + 1):
            if row[x_pos] != si_first_pixel:
                continue  # Pixel does not match.
            if row[x_pos:x_pos + si_width] != si_first_row:
                continue  # First row does not match.
            box = x_pos, y_pos, x_pos + si_width, y_pos + si_height
            with large_image.crop(box) as cropped:
                if list(cropped.getdata()) == si_pixels:
                    # We found our match!
                    return x_pos, y_pos


def find(large_image_path, subimg_path):
    """Take a screenshot and find the subimage within it.

    :param str subimg_path: Path to subimage file.
    """
    assert os.path.isfile(large_image_path)
    assert os.path.isfile(subimg_path)

    # Take screenshot.
    #with ImageGrab.grab() as rgba, rgba.convert(mode='RGB') as screenshot:
    #    print( find_subimage(screenshot, subimg_path) )
    
    #
    #png = Image.open(object.logo.path)
    #png.load() # required for png.split()

    #background = Image.new("RGB", png.size, (255, 255, 255))
    #background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
     
    #
    image = Image.open(large_image_path)            
    
    #
    print( find_subimage(image, subimg_path) )
    
    
def resize( path, res, FLAGS ):
    for item in dirs:
        print(item)
        if item == '.DS_Store':
            continue

        if os.path.isfile(path+item):
            f, e = os.path.splitext(item)

            #
            #find( path+item, FLAGS.object_image )

            #
            #image = cv2.imread(path+item)  
            #template = cv2.imread( FLAGS.object_image )  
            #result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)  
            #y, x = np.unravel_index(result.argmax(),result.shape)
            #print( "x=" + str( x ) + ", y=" + str(y) )
            
            #
            img = cv2.imread( path+item, 0 )
            img2 = img.copy()
            template = cv2.imread( FLAGS.object_image, 0 )
            w, h = template.shape[::-1]

            # All the 6 methods for comparison in a list
            methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                        'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

            for meth in methods:
                img = img2.copy()
                method = eval(meth)

                # Apply template Matching
                res = cv2.matchTemplate(img,template,method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)

                cv2.rectangle(img,top_left, bottom_right, 255, 2)

                plt.subplot(121),plt.imshow(res,cmap = 'gray')
                plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                plt.subplot(122),plt.imshow(img,cmap = 'gray')
                plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                plt.suptitle(meth)

                plt.show()
            
            
            #np.unravel_index(result.argmax(),result.shape)
            res[f] = "x=" + str( x ) + ", y=" + str(y)

    return res
            
            
res = {}            
for path in paths:
    dirs = os.listdir( path )
    res = resize( path, res, FLAGS )
    
#res
print(res)
