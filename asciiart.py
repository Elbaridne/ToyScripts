from PIL import Image
import numpy as np
import sys

# Retrieving command line arguments
if len(sys.argv) != 4:
    print('Use -> python asciiart.py <"image_path"> <reverse:0/1> <mode:0(Luminosity)/1(Average)>')
    sys.exit(0)
else:
    image_url = str(sys.argv[1])
    reverse_flag = bool(int(sys.argv[2]))
    mode = bool(int(sys.argv[3]))


resize_width = 180
resize_height = 140

# Opening and Resizing Image
try:
    image = Image.open(image_url)
    height, width = image.size
    image = image.resize([resize_width,resize_height])
    image_ar = np.asarray(image)

    # In case the image file doesn't exists or an error occurs during resizing we exit the script
except Exception as e:
    print(str(e))
    sys.exit(0)

# if reverse_flag, 255 -> 0    0->255
def reverse(value):
    return 255 - value

ord_ascii = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Maps each pixel to it's corresponding brightness ascii value
def map_ascii(value):
    if reverse_flag:
        value = reverse(value)

    #Edge cases (Both throw an exception, might as well handle them directly)
    if value == 0:
        return ord_ascii[0]
    if value == 255:
        return ord_ascii[-1]

    rate = 255 / len(ord_ascii)
    num = int(value // rate)
    return ord_ascii[num]


'''
    Each image is stored 2 dim matrix 
    We transform each tuple (pixel) to an ascii char
    [(255,255,255), (255,255,255)... -> $, $
    [(128,128,255), (255,255,129)... -> @, $
    
'''
def print_image():
    for col in image_ar:
        for tuple in col:
            if not mode:
                avg = sum(tuple)/3
                print(map_ascii(avg), end='')
            if mode:
                luminosity = tuple[0] * 0.21 + tuple[1] * 0.72 + tuple[2] * 0.07
                print(map_ascii(luminosity), end='')

        print("")

print_image()

