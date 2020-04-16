## Toolbox 

This repo contains tools used for my personal needs.

### Scripts:

1. `extract_slides_from_video.py`: 
   1. **Usage**: extract slides from video lecture, where the video contains a series of slides transition;
   2. **Method**: extract current frame as new slide, if changes from previous frame to current frame is detected (checking frequency: 1 frame/sec, no matter of the frame rate is)
   3. **Output**: 
      1. individual images (.jpg) as slides in a folder with the same name of the video file in the same directory;
      2. single .pdf file per video lecture, with merged slides together.
2. `make_passport_collage.py`:
   1. **Usage**: make 4X6 collage photo from 6 2X2 photos, so it can be easily ordered online for print
   2. **Details**:
      1. It requires 6 copies of 2X2 photos, if the number of available image is fewer than 6, make copies; if there are more than 6, only the first 6 in sorted order will be used;
      2. It does not matter if the 2X2 photos are in different resolution, as long as they are square. They will be all resized into the same size (default: 20000X2000) before combining.
3. `screenshot2slide.py`:
   1. **Usage**: convert screenshots to slides by specifying the crop location and size  (i.e. the coordinate of the left-top corner and right-bottom corner)
   2. **Use cases**:
      1. *Case 1*: assume you have saved a few screenshots of presentation slides from a video course, but the slides are not in full-screen size. If this is the case, you may want to check the size of the location of the slides in screenshots, and use this script to extract the slides from screenshot images.
      2. *Case 2*: After a running event, you received link to preview all your photos in small size and watermark. You don't want to pay the expensive price but still want to save a copy of these photos in smaller version. Then, you may take screenshots and then use this script to process.
   3. **Details**: change the image directories and capture location and size information before running.

