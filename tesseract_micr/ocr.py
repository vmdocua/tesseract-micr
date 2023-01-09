import logging
import logging.config
import sys
import os
import pytesseract;

from core import app_config

logger = logging.getLogger(__name__)

class TesseractOcr:

    def __int__(self):
        pass

    def ocrPlain(self, path):
        logger.debug(f'ocrPlain(path={path})')
        res = pytesseract.image_to_string(path)
        logger.debug("-> "+res)
        return res

    def ocrMicr(self, path):
        logger.debug(f'ocrMicr(path={path})')
        tessdataPath = os.path.join(app_config.ROOT_PATH, "tessdata")
        cfg = f" --tessdata-dir {tessdataPath}" \
              " -l micr --psm 6" \
              " -c tessedit_char_whitelist=0123456789acd "
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_string(path, lang='micr', config=cfg)
        logger.debug("-> "+res)
        return res

    def ocrMicrHocr(self, path):
        logger.debug(f'ocrMicrHocr(path={path})')
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
        #logger.debug("-> "+res)
        return res

    def version(self):
        return "tesseract {}".format(pytesseract.get_tesseract_version())


