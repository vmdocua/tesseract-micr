import logging
import logging.config
import sys
import os
import pyvips;

from tesseract_micr.core import app_config

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

    def chain(self, path, commands):
        logger.debug(f"chain(commands={commands})")
        lst = commands.split("|")
        res = path
        for cmd in lst:
            logger.debug("cmd="+cmd)
            args = []
            name = cmd
            i = cmd.find("(")
            if i >= 0:
                name = cmd[:i]
                a = cmd[i:].strip("() ")
                args = a.split(",")

            f = getattr(self, name)
            if len(args) == 0:
                res = f(res)
            elif len(args) == 1:
                res = f(res, args[0])
            elif len(args) == 2:
                res = f(res, args[0], args[1])
            elif len(args) == 3:
                res = f(res, args[0], args[1], args[2])
            else:
                assert "Unsupported, cmd.length="+cmd.length

        return res

    def load(self, pathOrData):
        if isinstance(pathOrData, bytes):
            image = pyvips.Image.new_from_buffer(pathOrData, "")
        else:
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
        image = image.relational_const("moreeq", int(threshold))
        return self.toBuffer(image)

    def vipsVersion(self):
        return "vips-{}.{}.{}".format(pyvips.version(0), pyvips.version(1), pyvips.version(2))
