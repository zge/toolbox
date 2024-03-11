# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:56:57 2023

Utilities used for zge/Study/Programming/Python/toolbox/finance

@author: gezhe
"""

def convert_symbol(text, l1, l2, quote='"'):
  """convert symbol l1 to l2 if inside quote"""
  text2 = ''
  inside = False
  for c in text:
    if c == quote:
      inside = not inside
    elif c == l1:
      if inside:
        text2 += l2
      else:
        text2 += l1
    else:
       text2 += c
  return text2

def csv2dlist(csvname, delimiter=','):
    """extract rows in csv file to a dictionary list"""
    lines = open(csvname, 'r').readlines()
    header = lines[0].rstrip().split(delimiter)
    lines = lines[1:]
    nlines = len(lines)

    dict_list = [{} for _ in range(nlines)]
    for i, line in enumerate(lines):
        line2 = convert_symbol(line.rstrip(), delimiter, '|')
        items = line2.split(delimiter)
        items = [s.replace('|', delimiter) for s in items]
        dict_list[i] = {k:items[j] for j,k in enumerate(header)}

    return dict_list