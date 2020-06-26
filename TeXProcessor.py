import io

import matplotlib.pyplot as plt
from PIL import Image, ImageChops

white = (90, 90, 90, 255)


def latex_to_img(tex):
    buf = io.BytesIO()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.axis('off')
    plt.text(0.05, 0.5, r'${}$'.format(tex), size=40)
    plt.savefig(buf, format='png')
    plt.close()

    im = Image.open(buf)
    bg = Image.new(im.mode, im.size, white)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()

    return im.crop(bbox)


def create_png(string, filename='temp.png'):
    return latex_to_img(string).save(filename)



