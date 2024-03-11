# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import os
import argparse
from sys import platform

from utils import csv2dlist

def convert_entries(dlist):
  """convert entries in dict list to a new one with info we need
  1. combine debit/credit into one column
  2. disregard "status" column
  """
  nentries = len(dlist)
  
  dlist2 = [[] for _ in range(nentries)]
  for i, d in enumerate(dlist):
    if dlist[i]['Debit']:
      amount = float(dlist[i]['Debit'])
    else:
      amount = float(dlist[i]['Credit'])
    dlist2[i] = {'Date': dlist[i]['Date'],
                 'Description': dlist[i]['Description'],
                 'Amount': amount,
                 'Member': dlist[i]['Member Name']}
  return dlist2

def add_type(dlist):
    """add type column to differenciate regular/refund/payment transactions"""

  
def get_rootdir(directory):
  if platform == "linux" or platform == "linux2":
    rootdir = os.path.join(r'/home/users/zge/Dropbox', directory.replace("\\","/"))
  elif platform == "darwin":
    rootdir = os.path.join(r'/Users/zhenhaoge/Dropbox', directory.replace("\\","/"))
  elif platform == "win32":
    rootdir = os.path.join(r'C:\Users\gezhe\Dropbox', directory.replace("/", "\\"))
  return rootdir  

def parse_args():
  usage = 'usage: example to process citi transaction csv file'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('--csvfile', type=str)
  
  return parser.parse_args()

if __name__ == '__main__':
  
  # runtime mode
  args = parse_args()
  
  # interactive mode
  args = argparse.ArgumentParser()
  rootdir = get_rootdir(r'zge\Daily\Financial\BankAccounts')
  assert os.path.isdir(rootdir), "root dir: {} doesn't exist!".format(rootdir)
  folders = ['Citi - Costco','transactions']
  csvfn = r'20230101-20230421_citi-costco_transactions.CSV'
  args.csvfile = os.path.join(rootdir, *folders, csvfn)
  assert os.path.isfile(args.csvfile), "CSV file: {} doesn't exist!".format(args.csvfile)
  
  dlist = csv2dlist(args.csvfile)
  dlist2 = convert_entries(dlist)

    
  
  
