# -*- coding: utf-8 -*-
"""
Rename files

Zhenhao Ge, 2021-12-04
"""

import glob
import os

datadir = r'F:\Photos\Lightroom\2021\2021-12-03\Video'
ext = 'MP4'
prefix = '20211203'

filenames = glob.glob(os.path.join(datadir, '*.{}'.format(ext)))
filenames = [f for f in filenames if prefix not in f]
print('change {} file names ...'.format(len(filenames)))

for f in filenames:
  src = f
  filename = os.path.basename(f)
  filedir = os.path.dirname(f)
  filename2 = '{}-{}'.format(prefix,filename)
  dst = os.path.join(filedir, filename2)
  os.rename(src,dst)
