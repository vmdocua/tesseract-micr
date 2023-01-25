import io
import logging
import logging.config
import sys
import os
import PIL
from PIL import Image
from PIL import ImageOps
import pyvips


from docsultant.core import app_config

logger = logging.getLogger(__name__)

class ImageProcessor:

    #: default output format
    OUT_VIPS_FORMAT = ".tif"
    OUT_PIL_FORMAT = "TIFF"

    #: default output mime type
    OUT_MIME_TYPE = "image/tiff"

    """
    def border(self, path, width=12):
        logger.debug("border(...,{})".format(width))
        image = self.pil_load(path)
        image = ImageOps.expand(image, border=width, fill="white")
        data = self.toBuffer(image)
        return data
    """

    def border(self, path, width: int = 20):
        logger.debug("border(...,{})".format(width))
        width = int(width)
        image = self.vips_load(path)
        image2 = pyvips.Image.black(width*2 + image.width, width*2 + image.height, bands=image.bands)
        image2 = pyvips.Image.invert(image2)
        image2 = pyvips.Image.insert(image2, image, width, width)
        # logger.debug("interpretation="+image.interpretation)
        return self.to_buffer(image2)

    def bw(self, path):
        logger.debug("bw(...)")
        image = self.vips_load(path)
        image = image.colourspace("b-w")
        return self.to_buffer(image)

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

    def invert(self, path, width: int = 20):
        logger.debug("invert(...,{})".format(width))
        width = int(width)
        image = self.vips_load(path)
        image = pyvips.Image.invert(image)
        return self.to_buffer(image)

    def vips_load(self, pathOrData) -> pyvips.Image:
        pathOrData = self.to_vips(pathOrData)
        if isinstance(pathOrData, bytes):
            image = pyvips.Image.new_from_buffer(pathOrData, "")
        else:
            image = pyvips.Image.new_from_file(pathOrData, access="sequential")
        return image

    def pil_load(self, pathOrData):
        pathOrData = self.to_pil(pathOrData)
        if isinstance(pathOrData, bytes):
            image = Image.open(io.BytesIO(pathOrData))
        else:
            image = Image.open(pathOrData)
        return image

    def to_pil(self, pathOrData):
        if isinstance(pathOrData, pyvips.Image):
            return self.to_buffer(pathOrData)
        return pathOrData

    def to_vips(self, pathOrData):
        if isinstance(pathOrData, PIL.Image.Image):
            return self.to_buffer(pathOrData)
        return pathOrData

    def to_buffer(self, image):
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
        image = self.vips_load(path)
        image = image.rot("d{}".format(angle))
        return self.to_buffer(image)

    def scale(self, path, factor: float = 1.0):
        logger.debug("scale(...,{})".format(factor))
        factor = float(factor)
        image = self.vips_load(path)
        image = pyvips.Image.resize(image, factor)
        return self.to_buffer(image)

    def sharpen(self, path):
        logger.debug("sharpen(...)")
        image = self.vips_load(path)
        image = image.sharpen()
        return self.to_buffer(image)

    def threshold(self, path, threshold):
        logger.debug(f"threshold(.., threshold={threshold})")
        image = self.vips_load(path)
        image = image.relational_const("moreeq", int(threshold))
        return self.to_buffer(image)

    def vips_version(self):
        return "vips-{}.{}.{}".format(pyvips.version(0), pyvips.version(1), pyvips.version(2))
