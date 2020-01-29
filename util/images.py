import os
from apng import APNG


def stitch_screenshot(path):
    img_files = [f for f in os.listdir(path) if f.endswith('.png')]
    img_files.sort()
    im = APNG()
    for file in img_files:
        im.append_file(path + '/' + file)
    im.save(path + '/' + img_files[0] + '.png')
    for file in img_files:
        os.remove(path + '/' + file)
