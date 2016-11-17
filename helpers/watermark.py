
from imagekit.lib import Image


class ImageWatermark(object):

    def __init__(self, watermark_path):
        self.watermark_path = watermark_path

    def process(self, img):

        # get watermark
        wm = Image.open(self.watermark_path)
        wm_size = wm.size

        # prepare image for overlaying (ensure alpha channel)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # create a layer to place the watermark
        layer = Image.new('RGBA', img.size, (0,0,0,0))
        coords = (img.size[0] - wm_size[0] - 20, img.size[1] - wm_size[1] - 20)

        layer.paste(wm, coords)


        img = Image.composite(layer, img, layer)

        return img