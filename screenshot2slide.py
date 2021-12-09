# -*- coding: utf-8 -*-
"""
Convert screenshots to slides by specifying the crop size

Zhenhao Ge, 2019-03-05
"""

import glob
import os
from PIL import Image

# parameters need to be specified

## setting 1
#imgext = 'png'
#nscreens = 1
#screenidx = 1 # start from 0
#img_dir = r'C:\Users\zge\Dropbox\zge\Study\Programming\Python\utilities\imgs'
#left_top = (2822, 350)
#right_bottom = (3161, 863)

# setting 2
#img_dir = r'C:\Users\zge\Dropbox\zge\Photos\SIE\Holiday'
img_dir = r'C:\Users\zge\Dropbox\Screenshots\2021-03-11'

imgext = 'png'
nscreens = 3
screenidx = 1 # start from 0
left_top = (0,0)
right_bottom = (1920, 1080)
#left_top = (52, 103)
#right_bottom = (1546, 941)

def get_screen(img, nscreens, screenidx):
  """extract screen from image"""
  width, height = img.size
  width_per_screen = int(width/nscreens)
  left = int(width_per_screen*screenidx)
  right = left + width_per_screen
  top, bottom = 0, height
  screenimg = img.crop((left,top,right,bottom))
  return screenimg

directory = {}
directory['work'] = img_dir
directory['par'] = os.path.dirname(directory['work'])
directory['output'] = os.path.join(directory['par'], 'outputs')
if not os.path.isdir(directory['output']):
  print('creating dir: {}'.format(directory['output']))
  os.makedirs(directory['output'])

imgfiles = sorted(glob.glob(os.path.join(directory['work'], '*.{}'.format(imgext))))
imgnames = [os.path.basename(f) for f in imgfiles]
nimgs = len(imgfiles)
print('# of images: {}'.format(nimgs))

img = Image.open(imgfiles[0])
width, height = img.size

left, top = left_top
right, bottom = right_bottom
for i in range(nimgs):
  print('processing image {}: {} ...'.format(i, imgnames[i]))
  img = Image.open(imgfiles[i])
  #img.show()
  subimg = get_screen(img, nscreens, screenidx)
  subimg2 = subimg.crop((left,top,right,bottom))
  outfile = os.path.join(directory['output'], imgnames[i])
  subimg2.save(outfile)