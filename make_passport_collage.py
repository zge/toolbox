#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make 4X6 collage with 6 2X2 photos

Currently requires 6 copies of 2X2 photos, if the number of available
images is smaller than 6, make copies first

Images can be in different sizes, as long as they are square image
Later all 6 images will be resized to the same size.

Zhenhao Ge, 2019-06-07
"""

import glob
import os
#from pathlib import Path
from PIL import Image
from scipy.misc import imresize, imsave
#from skimage.transform import resize
import numpy as np
import argparse

def parse_args():

  usage = "usage: make 4X6 collage with 6 2X2 photos"
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('--img-dir', type=str)
  parser.add_argument('--out-img', type=str, default='collage.jpg')
  parser.add_argument('--prefix', type=str, default='',
                      help='prefix in image filenames')
  parser.add_argument('--resolution', type=int, default=2000,
                      help='pixel in width and height')

  return parser.parse_args()

args = parse_args()

# parameters need to be specified
img_dir = args.img_dir
#home = str(Path.home())
#img_dir = os.path.join(home, 'Dropbox', 'zge', 'People', 'Muyang Ge', 'photo',
#                       'collage_20190607')
#left_top = (2822, 350)
#right_bottom = (3161, 863)

nimgs = 6

prefix = args.prefix
#prefix = 'passport_'
imgfiles = sorted(glob.glob(os.path.join(img_dir, '{}*.jpg'.format(prefix))))
if len(imgfiles) < nimgs:
  raise Exception('# images to combine should be no fewer than {}!'.format(nimgs))
imgnames = [os.path.basename(f) for f in imgfiles[:nimgs]]
print('# of images: {}'.format(nimgs))

# read and resize image to the same size
width0, height0 = args.resolution, args.resolution
imgs = [[] for _ in range(nimgs)]
for i in range(nimgs):
  imgs[i] = Image.open(imgfiles[i])
  width, height = imgs[i].size
  print('image {}: width {}, height {}'.format(i, width, height))
  imgs[i] = imresize(imgs[i], (width0, height0))
  #imgs[i] = resize(np.array(imgs[i]), (width0, height0))

# concatenate images
nrows, ncols = 2, 3
img = np.zeros((height0*nrows, width0*ncols, 3), dtype='uint8')
for i in range(nimgs):
  idx_row = int(i/ncols)
  idx_col = i % ncols
  img[idx_row*height0:(idx_row+1)*height0,
      idx_col*width0: (idx_col+1)*width0,:] = imgs[i]

# save image
outpath = os.path.join(img_dir, args.out_img)
imsave(outpath, img)