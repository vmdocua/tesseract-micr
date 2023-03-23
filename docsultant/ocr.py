import logging
import logging.config
import sys
import os
import io
import re
import pytesseract
from PIL import Image, ImageDraw, ImageFont

from docsultant.imgproc import ImageProcessor
from docsultant.hocr import HocrParser
from docsultant.core import app_config

logger = logging.getLogger(__name__)

class TesseractOcr:

    def __init__(self):
        self.imgProc = ImageProcessor()

    def box_scale(self, path_in: str, path_out: str, scale: float) -> str:
        logger.debug("box_scale(..., path_in={}, path_out={}, scale={})".format(path_in, path_out, scale))
        # box line= <symbol> <left> <bottom> <right> <top> <page>
        with open(path_in) as f:
            with open(path_out, 'w', encoding='utf-8') as f2:
                lines = [line.rstrip() for line in f]
                for line in lines:
                    logger.debug(line)
                    a = line.split(" ")
                    a[1] = self.box_scale_scale(a[1], scale)
                    a[2] = self.box_scale_scale(a[2], scale)
                    a[3] = self.box_scale_scale(a[3], scale)
                    a[4] = self.box_scale_scale(a[4], scale)
                    line2 = " ".join(a)
                    logger.debug(" -> "+line2)
                    f2.write(line2)
                    f2.write('\n')

        return "Done"

    def box_scale_scale(self, coord: str, scale: float) -> str:
        return str(int(int(coord)*float(scale)))

    def generate_box_image(self, path_font: str, font_size: int, font_mode, path_gt: str,
                           path_tif: str, path_box: str, scale: int) -> str:

        margin: int = 30
        # read text to draw
        text = ""
        with open(path_gt) as f:
            text = f.read()
        line_count = text.count('\n')+1

        # get font
        font = ImageFont.truetype(path_font, font_size)
        ascent, descent = font.getmetrics()

        # text_w = font.getmask(text).getbbox()[2]
        # text_h = line_count*(font.getmask(text).getbbox()[3] + descent)
        text_w, text_h = font.getsize_multiline(text)
        logger.debug(f"text_w={text_w}, text_h={text_h}")

        image = Image.new("RGB", (text_w + margin*2, text_h + margin*2 ), "white")
        draw = ImageDraw.Draw(image)
        if font_mode:
            draw.fontmode = font_mode

        draw.text((margin, margin), text, font=font, fill="black")


        if scale>1:
            image = image.resize([image.width*scale, image.height*scale], Image.NEAREST)

        image.save(path_tif, format="TIFF")

        return f"Done.\n\nImage: {path_tif}\nBox: {path_box}"

    def hocr_visualize_as_png(self, path, chain: str, doc: HocrParser.Document) -> bytes:
        logger.debug("hocr_visualize_as_png(..., path={}, chain={})".format(path, chain))
        image: Image = None
        if chain:
            image = self.imgProc.chain(path, chain)
        else:
            image = self.imgProc.to_buffer(self.imgProc.vips_load(path))

        image = Image.open(io.BytesIO(image))

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("Arial", 16)
        for w in doc.words:
            rc = [w.bbox.left, w.bbox.top, w.bbox.right, w.bbox.bottom]
            draw.rectangle(rc, outline="red")
            txt = re.sub(r"[^a-zA-Z0-9]", " ", w.text)
            draw.text((w.bbox.left, w.bbox.top), txt, font=font, fill="blue", align="center")

        b = io.BytesIO()
        image.save(b, format="PNG")
        b.seek(0)
        data = b.read()
        return data


    def ocr_check(self, path, chain="sharpen|threshold(140)|bw") -> str:
        logger.debug(f'ocr_check(path={path})')
        img = self.imgProc.chain(path, chain)
        img = Image.open(io.BytesIO(img))
        doc = self.tesseract_micr_hocr(img)
        # TODO: do preliminary regexp filtering
        return "\n".join([line.text for line in doc.lines])

    def tesseract_plain(self, path, chain) -> str:
        logger.debug(f'tesseract_plain(path={path})')
        if chain:
            img = self.imgProc.chain(path, chain)
            path = Image.open(io.BytesIO(img))
        res = pytesseract.image_to_string(path)
        logger.debug("-> "+res)
        return res

    def tesseract_hocr(self, path, chain) -> HocrParser.Document:
        logger.debug(f'tesseract_hocr(path={path})')

        if chain:
            img = self.imgProc.chain(path, chain)
            path = Image.open(io.BytesIO(img))

        # psm 4, psm 6
        cfg = f" -c hocr_char_boxes=1" \
              " hocr"
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_pdf_or_hocr(path, config=cfg, extension='hocr')
        res = res.decode('utf-8')

        hp = HocrParser()
        doc = hp.parse(res)
        return doc


    def tesseract_micr(self, path) -> str:
        logger.debug(f'tesseract_micr(path={path})')
        tessdataPath = os.path.join(app_config.ROOT_PATH, "tessdata")
        cfg = f" --tessdata-dir {tessdataPath}" \
              " -l micr --psm 6" \
              " -c tessedit_char_whitelist=0123456789acd "
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_string(path, lang='micr', config=cfg)
        logger.debug("-> "+res)
        return res

    def tesseract_micr_hocr(self, path) -> HocrParser.Document:
        logger.debug(f'tesseract_micr_hocr(path={path})')
        tessdataPath = os.path.join(app_config.ROOT_PATH, "tessdata")
        cfg = f" --tessdata-dir {tessdataPath}" \
              " -l micr --psm 6" \
              " -c tessedit_char_whitelist=0123456789acd " \
              " -c hocr_char_boxes=1" \
              " -c lstm_choice_mode=1" \
              " -c tessedit_pageseg_mode=6" \
              " hocr"
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_pdf_or_hocr(path, \
                     lang='micr', config=cfg, extension='hocr')
        res = res.decode('utf-8')

        hp = HocrParser()
        doc = hp.parse(res)
        #logger.debug("-> "+res)
        return doc

    def tesseract_version(self):
        return "tesseract {}".format(pytesseract.get_tesseract_version())


