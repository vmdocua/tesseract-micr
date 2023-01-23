import io
import logging
import logging.config
import sys
import os
import PIL
from PIL import Image
from PIL import ImageOps
import pyvips


from tesseract_micr.core import app_config

logger = logging.getLogger(__name__)

class ImageProcessor:

    #: default output format
    OUT_VIPS_FORMAT = ".tif"
    OUT_PIL_FORMAT = "TIFF"

    #: default output mime type
    OUT_MIME_TYPE = "image/tiff"

    def border(self, path, width=12):
        logger.debug("border(...,{})".format(width))
        image = Image.open(path)
        image = ImageOps.expand(image, border=width, fill="white")
        data = self.toBuffer(image)
        return data

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
        if isinstance(image, pyvips.Image):
            data = image.write_to_buffer(self.OUT_VIPS_FORMAT)
            return data
        elif isinstance(image, PIL.Image.Image):
            b = io.BytesIO()
            image.save(b, format=self.OUT_PIL_FORMAT)
            b.seek(0)
            data = b.read()
            return data
        return None

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
