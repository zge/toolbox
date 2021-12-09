# convert subtitles from .srt to .txt format
# by simply remove timestamps and blank lines
#
# Zhenhao Ge, 2015-03-10

import os, sys
#import glob
import fnmatch
import codecs

args = sys.argv[1:]
refresh = False
if len(args) > 0 and args[0] == '--refresh':
    refresh = True
    del args[0]
elif len(args) > 0 and args[0] == '--help':
    print('convert subtitles from .srt to .txt format')
    print('usage: [--refreseh] directory (optional)')
    sys.exit(1)
    
directory = {}
directory['current'] = os.getcwd()
if len(args) > 0:
    directory['work'] = args[0]   
else:
    if os.name == 'nt':
        dirs = [r'\\\\psf\Dropbox\Study\Language\Chinese\Red\subtitles',
                r'D:\Dropbox\Study\Language\Chinese\Red\subtitles']
        for url in dirs:
            if os.path.isdir(url):
                directory['work'] = url
                break
        #directory['work'] = r'\\\\psf\Dropbox\Study\Language\Chinese\Red\subtitles'
    elif os.name == 'posix':
        dirs = [r'/Users/zge/Dropbox/Study/Language/Chinese/Red/subtitles',
                r'/cygdrive/d/Dropbox/Study/Language/Chinese/Red/subtitles',
                os.path.join(os.getenv("HOME"), 
                    r'Dropbox/Study/Language/Chinese/Red/subtitles'),]
        for url in dirs:
            if os.path.isdir(url):
                directory['work'] = url
                break
        #directory['work'] = r'/Users/zge/Dropbox/Study/Language/Chinese/Red/subtitles'
    else:
        print(os.name)
        sys.exit(1)
if directory['current'] != directory['work']:
    print('work directory:', directory['work'])
    os.chdir(directory['work'])
    
#matches = glob.glob("*.srt")
matches = []
for root, dirnames, filenames in os.walk(directory['work']):
  for filename in fnmatch.filter(filenames, '*.srt'):
    matches.append(os.path.join(root, filename))

cnt1, cnt2 = 0, 0
for file in matches:
    source = codecs.open(file, 'rb', encoding='utf-8')
    file2 = os.path.splitext(file)[0] + '.txt'
    if os.path.isfile(file2) and refresh == False:
        print(file2, 'existed')
        cnt1 += 1
    else:
        out = codecs.open(file2, 'wb', encoding='utf-8')
        #lines = source.readlines()       
        
        for line in source:
            if not (line[0].isdigit() or line=='\r\n' or line[0]==u'\ufeff'):
                #print(line[:-2], end='\n')
                #line
                out.write(line)
        print(file2, 'created')
        out.close()
        cnt2 += 1
    source.close()

if refresh == False:
    print(str(len(matches)), 'processed,', str(cnt1), 'already existed,', 
      str(cnt2), 'newly created.')    
else:
    print('refresh all:', str(cnt2), 'newly created')    
      