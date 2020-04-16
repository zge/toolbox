# -*- coding: utf-8 -*-
"""
Convert screenshots to slides by specifying the crop size

Zhenhao Ge, 2019-03-05
"""

import glob
import os
from PIL import Image

# parameters need to be specified
img_dir = r'C:\Users\zge\Dropbox\zge\Study\Programming\Python\utilities\imgs'
left_top = (2822, 350)
right_bottom = (3161, 863)

directory = {}
directory['work'] = img_dir
directory['par'] = os.path.dirname(directory['work'])
directory['output'] = os.path.join(directory['par'], 'outputs')
if not os.path.isdir(directory['output']):
  print('creating dir: {}'.format(directory['output']))
  os.makedirs(directory['output'])

imgfiles = sorted(glob.glob(os.path.join(directory['work'], '*.png')))
imgnames = [os.path.basename(f) for f in imgfiles]
nimgs = len(imgfiles)
print('# of images: {}'.format(nimgs))

img = Image.open(imgfiles[0])
width, height = img.size

left, top = left_top
right, bottom = right_bottom
for i in range(nimgs):
  print('processing image {}: {} ...'.format(i, imgnames[i]))
  img = Image.open(imgfiles[i]).crop((left,top,right,bottom))
  outfile = os.path.join(directory['output'], imgnames[i])
  img.save(outfile)