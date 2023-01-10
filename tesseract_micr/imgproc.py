import logging
import logging.config
import sys
import os
import pyvips;

from core import app_config

logger = logging.getLogger(__name__)

class ImageProcessor:

    #: default output format
    OUT_FORMAT    = ".tif"

    #: default output mime type
    OUT_MIME_TYPE = "image/tiff"

    def bw(self, path):
        logger.debug("bw(...)")
        image = self.load(path)
        image = image.colourspace("b-w")
        return self.toBuffer(image)

    def load(self, pathOrData):
        image = pyvips.Image.new_from_file(pathOrData, access="sequential")
        return image

    def toBuffer(self, image):
        data = image.write_to_buffer(self.OUT_FORMAT)
        return data

    def rotate(self, path, angle):
        logger.debug(f"rotate(.., angle={angle})")
        image = self.load(path)
        image = image.rot("d{}".format(angle))
        return self.toBuffer(image)

    def sharpen(self, path):
        logger.debug("sharpen(...)")
        image = self.load(path)
        image = image.sharpen()
        return self.toBuffer(image)

    def threshold(self, path, threshold):
        logger.debug(f"threshold(.., threshold={threshold})")
        image = self.load(path)
        image = image.relational_const("moreeq", threshold)
        return self.toBuffer(image)

    def version(self):
        return "vips-{}.{}.{}".format(pyvips.version(0), pyvips.version(1), pyvips.version(2))
