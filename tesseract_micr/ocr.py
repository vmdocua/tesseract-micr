import logging
import logging.config
import sys
import os
import io
import pytesseract
from PIL import Image
from tesseract_micr.imgproc import ImageProcessor
from tesseract_micr.hocr import HocrParser
from tesseract_micr.core import app_config

logger = logging.getLogger(__name__)

class TesseractOcr:

    def __init__(self):
        self.imgProc = ImageProcessor()

    def ocrCheck(self, path, chain="sharpen|threshold(140)|bw") -> str:
        logger.debug(f'ocrCheck(path={path})')
        img = self.imgProc.chain(path, chain)
        img = Image.open(io.BytesIO(img))
        doc = self.tesseractMicrHocr(img)
        # TODO: do preliminary regexp filtering
        return "\n".join([line.text for line in doc.lines])

    def tesseractPlain(self, path) -> str:
        logger.debug(f'tesseractPlain(path={path})')
        res = pytesseract.image_to_string(path)
        logger.debug("-> "+res)
        return res

    def tesseractMicr(self, path) -> str:
        logger.debug(f'tesseractMicr(path={path})')
        tessdataPath = os.path.join(app_config.ROOT_PATH, "tessdata")
        cfg = f" --tessdata-dir {tessdataPath}" \
              " -l micr --psm 6" \
              " -c tessedit_char_whitelist=0123456789acd "
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_string(path, lang='micr', config=cfg)
        logger.debug("-> "+res)
        return res

    def tesseractMicrHocr(self, path) -> HocrParser.Document:
        logger.debug(f'tesseractMicrHocr(path={path})')
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

    def tesseractVersion(self):
        return "tesseract {}".format(pytesseract.get_tesseract_version())


