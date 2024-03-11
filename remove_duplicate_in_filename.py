# Remove the duplicate in file name
# convert {DATE}-{DATE}-{FILEID}.jpg to {DATE}-{FILEID}.jpg
#
# Zhenhao Ge, 2022-11-21

import os
import glob

# folder = r'C:\Users\zge\OneDrive\Pictures\Lightroom Saved Photos\2022-10-08 Soccer Game'
folder = r'E:\Photos\Lightroom\2022\2022-10-08'

filepaths = glob.glob(os.path.join(folder, '*.jpg'), recursive=True)

for filepath in filepaths:
    filedir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    parts = filename.split('-')
    filename2 = '-'.join([parts[0], parts[-1]])
    if filename != filename2:
        filepath2 = os.path.join(filedir, filename2)
        print('rename {} --> {} in folder {}'.format(filename, filename2, filedir))
        os.rename(filepath, filepath2)
        

