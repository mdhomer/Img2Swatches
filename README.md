# Img2Swatches

Simple python script used to conveniently generate photoshop swatch files __.aco__ from image files, for use with Adobe Photoshop CC 2015.

Output swatches contain all unique colors within image file, sorted by HSV values.

_Written on Mac OS X El Capitan 10.11.5_

- Python 2.7.10

Utilises Python Imaging Library
https://pillow.readthedocs.io/en/3.3.x/


### __Usage:__
    `python img2swatches.py <imagefile> <...other image files if wanted>`

###### Output file names, will be:
    `swatches-<prefix of image file provided>.aco`

###### Using in photoshop:
The output swatch files can then be used in Photoshop CC 2015 by:
1. Window -> Swatches.
2. Swatches dropdown -> Load swatches...
3. Select colors-'imagefileprefix'.aco
