#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Split files by time (put files into subfolders named with different time intervals)
e.g. 20211205-1040 contains photos taken during time 10:40 to 10:50 on 2021-12-05

Input arguments (default):
  - srcdir: source dir, where the original images come from
  - dstdir: destination dir, where all the sub-folders with different time interval are located
  - ext (jpg): image file extension, e.g. jpg or JPG
  - starttime (None): start time from which the photos after that time will be put into sub-folders
    - None: no start time is used (i.e. no filtering based on start time)
    - yyyymmdd-hhmm, e.g. 20211205-0955
  - itvlmin (5): interval min that is used to split photos taken from different times into groups
    - support int values within (1, ..., 60 min) only
  
Example:
  python split_files_by_time.py \
    -- srcdir r'C:\\Users\\gezhe\\OneDrive\\Pictures\\src' \
    -- dstdir r'C:\\Users\\gezhe\OneDrive\\Pictures\\dst' \
    -- ext jpg \
    -- starttime 20211205-0945 \
    -- itvlmin 5  
    
To start, try to modify the inpt arguments as you need

Zhenhao Ge, 2021-12-06
'''

import os
import glob
from PIL import Image
import datetime
import shutil
import argparse

def get_basedir(strtime, itvlmin):
  dtime = datetime.datetime.strptime(strtime, '%Y:%m:%d %H:%M:%S')
  dstdir_min = dtime.minute // itvlmin * itvlmin
  basedir = '{}{:02d}{:02d}-{:02d}{:02d}'.format(dtime.year, dtime.month,
             dtime.day, dtime.hour, dstdir_min)
  return basedir

def parse_args():
  
  usage = 'usage: split files by time'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('--srcdir', type=str)
  parser.add_argument('--dstdir', type=str)
  parser.add_argument('--ext', type=str, default='jpg')
  parser.add_argument('--starttime', type=str, default=None)
  parser.add_argument('--itvlmin', type=int, default=5)
  
  return parser.parse_args()

if __name__ == '__main__':

  # runtime mode
  args = parse_args()
  
  # # interactive mode (change input arguments as you need)
  # args = argparse.ArgumentParser()
  # args.srcdir = r'C:\Users\gezhe\OneDrive\Pictures\src'
  # args.dstdir = r'C:\Users\gezhe\OneDrive\Pictures\dst'
  # args.ext = 'jpg' # photos extension
  # args.starttime = datetime.datetime(2021,12,5,9,45,0) # used to filter out photos taken before this time
  # args.itvlmin = 5 # interval min (current version upports from value 1 up to 60 min, i.e. 1 hour only)
  
  # get input arguments other than start time  
  srcdir = args.srcdir
  dstdir = args.dstdir
  ext = args.ext
  itvlmin = args.itvlmin
  
  # get start time
  if args.starttime:
    ymd, hm = args.starttime.split('-')
    year, month, day = int(ymd[:4]), int(ymd[4:6]), int(ymd[6:])
    hour, minute = int(hm[:2]), int(hm[2:4])
    starttime = datetime.datetime(year, month, day, hour, minute, 0)
  else:
    starttime = None
  
  print('src dir: {}'.format(srcdir))
  print('dst dir: {}'.format(dstdir))
  print('image file ext: {}'.format(ext))
  print('start time: {}'.format(starttime))
  print('interval min: {}'.format(itvlmin))
  
  # find all photos from the source dir
  os.makedirs(dstdir, exist_ok=True)
  imgfiles = glob.glob(os.path.join(srcdir, '*.{}'.format(ext)))
  nimgfiles = len(imgfiles)
  print('# of image files: {}'.format(nimgfiles))
  
  # find the mapping from photo file basename (no ext) to the photo taken time
  file2time = {}
  for i, imgfile in enumerate(imgfiles):
    basename = os.path.splitext(os.path.basename(imgfile))[0]
    takentime = Image.open(imgfile)._getexif()[36867]
    #print('[{}/{}] {}: {}'.format(i+1, nimgfiles, basename, takentime))
    file2time[basename] = takentime
  
  # filter the file based on start time
  if starttime: 
    file2time_filtered = {}  
    for basename in file2time.keys():
      takentime = file2time[basename] 
      dtime = datetime.datetime.strptime(takentime, '%Y:%m:%d %H:%M:%S')
      if dtime >= starttime:
        file2time_filtered[basename] = takentime
  else:
    file2time_filtered = file2time.copy()
  print('# of image files after filtering: {}'.format(len(file2time_filtered)))  
      
  # [optional] sort basenames in 1) ascending order of the taken time, then 2) basename
  # so the photos will be moved in this organized order
  file_n_time = [(k,v) for (k,v) in file2time_filtered.items()]
  file_n_time_sorted = sorted(file_n_time,
    key = lambda i: (datetime.datetime.strptime(i[1], '%Y:%m:%d %H:%M:%S'), i[0]))    
      
  # move photo files to the destination sub dir
  for (basename, takentime) in file_n_time_sorted:
    basedir = get_basedir(takentime, itvlmin)
    outdir = os.path.join(dstdir, basedir)
    os.makedirs(outdir, exist_ok=True)
    infile = os.path.join(srcdir, '{}.{}'.format(basename, ext))
    outfile = os.path.join(outdir, '{}.{}'.format(basename, ext))
    if os.path.isfile(outfile):
      print('{} exists, skip!'.format(outfile))
    else:
      print('{} with {} --> {}'.format(basename, takentime, basedir))
      shutil.move(infile, outfile)
    