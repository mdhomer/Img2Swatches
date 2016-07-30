#Img2swatches.py
#written by Mitchell D. Homer 2016.
#https://mdhomer.github.io

import sys, re, struct, colorsys
from PIL import Image

#conversion function for rgb values from stored 2 byte values
def RGBValueToRGBColor(value):
    return int(float(value)/float(256 - 1) * (2 ** (8 * 2) - 1))

#gather all unique RGB colors in image, sort by HSV and return.
def colorsInImage(image):
    colors_rgb = []
    pixels = image.load()
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            if pixels[x,y] not in colors_rgb:
                colors_rgb.append(pixels[x,y])
    colors_rgb.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
    return colors_rgb

#writing binary data to .aco file in (big-endian byte order '>')
def writeColorsToFile(file, colors):
    for version in (1, 2):
        file.write(struct.pack('>HH', version, len(colors)))
        for (i, color) in enumerate(colors):
            rgbValues = map(RGBValueToRGBColor, color) + [0]
            file.write(struct.pack('>H%sH' %(len(rgbValues)), 0, *rgbValues))
            if version == 2:
                swatchName = "Swatch %d\x00" %(i + 1)
                file.write(struct.pack('>I%ds' %(len(swatchName) * 2),
                    len(swatchName), '\x00' + '\x00'.join(swatchName)))
    file.close()

#check for at least 1 input file.
if len(sys.argv) <= 1:
    print "Error: Provide image files, for swatch generation."
    quit()
print "Generating swatches..."
for i in range(1, len(sys.argv)):
    try:
        im = Image.open(sys.argv[i]).convert('RGB')
        colors = colorsInImage(im)
        #output data to file.
        if len(colors) > 1:
            #get image filename, for making palette filename.
            name = re.search('(?=(\w+).\w+$)', sys.argv[i])
            if name.group(1):
                outfileName = "colors-" + name.group(1) + ".aco"
                with open(outfileName, 'wb') as f:
                    writeColorsToFile(f, colors)
                print "{: <70}".format(outfileName), "[%d/%d]" %(i, len(sys.argv) - 1)
    except IOError:
        print "Skipped file '", sys.argv[i], "' - IOError"
