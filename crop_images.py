# -*- coding: utf-8 -*-
"""
Crop images

Zhenhao Ge, 2021-11-14
"""

import glob
import os
from PIL import Image

img_dir = r'C:\Users\gezhe\Dropbox\zge\Daily\Baby\Piano\8889_TchGde_PrepA-images'
img_ext = 'jpg' # 'jpg' or 'png' 
left_top = (757,155)
right_bottom = (2547,1490)


directory = {}
directory['work'] = img_dir
directory['par'] = os.path.dirname(directory['work'])
directory['output'] = os.path.join(directory['par'], 'outputs')
if not os.path.isdir(directory['output']):
  print('creating dir: {}'.format(directory['output']))
  os.makedirs(directory['output'])
  
imgfiles = sorted(glob.glob(os.path.join(directory['work'], '*.{}'.format(img_ext))))
imgfiles = imgfiles[5:-2] # filter out some images at the beginning and end
imgnames = [os.path.basename(f) for f in imgfiles]
nimgs = len(imgfiles)
print('# of images: {}'.format(nimgs))

img = Image.open(imgfiles[0])
width, height = img.size
print('image dimension: width {}, height {}'.format(width, height))

left, top = left_top
right, bottom = right_bottom
for i in range(nimgs):
  print('processing image {}: {} ...'.format(i, imgnames[i]))
  img = Image.open(imgfiles[i]).crop((left,top,right,bottom))
  outfile = os.path.join(directory['output'], imgnames[i])
  img.save(outfile)