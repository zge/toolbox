# -*- coding: utf-8 -*-
"""
Extract slides from course video

Method: detect frame difference

Pckage need to be installed:
  opencv:
    opt 1: conda install -c menpo opencv
    opt 2: conda install -c conda-forge opencv

Zhenhao Ge, 2020-04-15
"""

import os
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import glob
from pathlib import Path
import img2pdf
import argparse

# setup parameters
pattern = 'slide-{0:03}.jpg'
blk_size = 500

def showimg(img):
  image = Image.fromarray(img, 'RGB');
  image.show()

def imgs2gif(imgs, gifname):
  images = [Image.open(img).convert('RGB') for img in imgs]
  images[0].save(gifname, save_all=True, append_images=images[1:])

def imgs2pdf(imgs, pdfname, verbose=True):
  with open(pdfname, 'wb') as f:
    f.write(img2pdf.convert(imgs))
  if verbose:
    print('wrote images to {}'.format(pdfname))

def plot_diff(diffs, pngname, verbose=True):
  plt.plot(diffs)
  plt.xlabel('frame index (1 frame / sec)')
  plt.ylabel('mean difference')
  plt.title('frame differences')
  plt.savefig(pngname)
  #diffs_sorted = sorted(diffs)[::-1]
  #plt.plot(diffs_sorted)
  if verbose:
    print('wrote diff plot to {}'.format(pngname))

def extract_slides(video_path):
  """
  check frames at rate of 1 frame per second, and if diff between previous and
  current frame is greater than 0, extract that frame as slide, merge all
  extracted slide images into pdf file.
  """

  # get output dir
  output_dir = os.path.splitext(video_path)[0]

  # get video file handler
  vidcap = cv2.VideoCapture(video_path)
  nframes = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  idxs = list(range(0,nframes,int(fps)))
  nidxs = len(idxs)

  # readthe  first image
  success,img1 = vidcap.read()
  #showimg(img1)
  #height, width = img1.shape[:2]

  # write the first slide
  nslides = 0 # count #slides extracted
  print('writing slide {}(frame {}) ...'.format(nslides, 0))
  output_path = os.path.join(output_dir, pattern.format(nslides))
  cv2.imwrite(output_path, img1);

  diffs = []
  for i in range(1,nidxs):

    # track status
    if i % blk_size == 1:
      lower, upper = i, min(i+blk_size-1, nidxs)
      print('processing: {}/{} ~ {}/{} ...'.format(lower, nidxs, upper, nidxs))

    # extract frame with specific frame index
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, idxs[i])
    sucess, img2 = vidcap.read()
    #showimg(img2)

    # pass black screen
    if np.max(img2) <= 1:
      continue

    # write frame as slide if mean diff > 0
    # note: np.mean() != sum(sum())/(width x height)
    diff = np.mean(abs(img1 - img2))
    if diff > 0:
      nslides += 1
      print('writing slide {} (frame {}) ...'.format(nslides, idxs[i]))
      output_path = os.path.join(output_dir, pattern.format(nslides))
      cv2.imwrite(output_path, img2)

    # post-processing
    diffs.append(diff)
    img1 = img2[:]

  # get smallest non-zero diff value (diff between the 2 most similar slides)
  diffs_no_zeros = [d for d in diffs if d!=0]
  print('smallest non-zero diff: {}'.format(min(diffs_no_zeros)))

  # plot and save diff plot
  pngname = os.path.join(output_dir, 'diff.png')
  plot_diff(diffs, pngname)

  # merge slide images into pdf file
  imgs = glob.glob(os.path.join(output_dir, 'slide*.jpg'))
  pdfname = os.path.join(str(Path(output_dir).parent),
    '{}.pdf'.format(os.path.basename(output_dir)))
  imgs2pdf(imgs, pdfname)

def parse_args():

  usage = "usage: extract slides from video frames by comparing the difference" \
    + " within the adjacent frames"
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('--video-dir', default=os.getcwd())

  return parser.parse_args()

def main():

  args = parse_args()

  # setup dir and file path (paramenters need to be specified)
  video_dir = args.video_dir
  print('processing videos in video dir: {}'.format(video_dir))
  #video_dir = r'C:\Users\zge\Dropbox\Video\Courses\edX_IBM_DeepLearning1'
  video_paths = glob.glob(os.path.join(video_dir, '*.mp4'))
  nvideos = len(video_paths)

  for i, video_path in enumerate(video_paths):

    print('[{}/{}] processing {} ...'.format(i+1, nvideos, video_path))

    # specify the output dir
    output_dir = os.path.splitext(video_path)[0]
    if not os.path.isdir(output_dir):
      print('creating dir: {}'.format(output_dir))
      os.makedirs(output_dir)

    # get the target pdf name
    pdfname = os.path.join(str(Path(output_dir).parent),
      '{}.pdf'.format(os.path.basename(output_dir)))

    # extract slides if the target pdf file does not exist
    if not os.path.isfile(pdfname):
      extract_slides(video_path)
    else:
      print('{} already exist, skip!'.format(pdfname))

if __name__ == '__main__':
  main()
