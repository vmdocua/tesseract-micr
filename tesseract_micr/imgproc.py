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
        data = image.write_to_buffer(self.OUT_FORMAT)
        return data

    def load(self, pathOrData):
        image = pyvips.Image.new_from_file(pathOrData, access="sequential")
        return image


    def rotate(self):
        return "TODO:rotate"

    def sharpen(self):
        return "TODO:sharpen"

    def threshold(self):
        return "TODO:threshold"

    def version(self):
        return "vips-{}.{}.{}".format(pyvips.version(0), pyvips.version(1), pyvips.version(2))
