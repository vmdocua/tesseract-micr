import logging
import logging.config
import sys
import os
import pyvips;

from core import app_config

logger = logging.getLogger(__name__)

class ImageProcessor:

    def bw(self):
        return "TODO:bw"

    def rotate(self):
        return "TODO:rotate"

    def sharpen(self):
        return "TODO:sharpen"

    def threshold(self):
        return "TODO:threshold"

    def version(self):
        return "vips-{}.{}.{}".format(pyvips.version(0), pyvips.version(1), pyvips.version(2))
