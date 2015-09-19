from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
import pylab
import sys

dino = Image.open(r"F:\PY\data\051_0066.jpg")

def showImage():
    pylab.imshow(dino)
    pylab.show()

def showHistogram():
    hist = dino.histogram()
    pylab.hist(hist,bins=40)
    pylab.show()

def showImageFilter():
    im1 = dino.filter(ImageFilter.BLUR)
    im2 = dino.filter(ImageFilter.FIND_EDGES)
    im3 = dino.filter(ImageFilter.EDGE_ENHANCE_MORE)
    im4 = dino.filter(ImageFilter.CONTOUR)
    pylab.imshow(im4)
    pylab.show()

def showImageOps():
    im = ImageOps.invert(dino)
    im1 = ImageOps.grayscale(dino)
    im2 = ImageOps.solarize(dino,threshold = 128)
    pylab.imshow(im2)
    pylab.show()

def showImageTranspose():
    im = dino.transpose(Image.ROTATE_270)
    im2 = dino.crop((20,20,200,100))
    pylab.imshow(im2)
    pylab.show()


def main():
    #showImageFilter()
    #showImageOps()
    showImageTranspose()

if __name__ == "__main__":
    main()