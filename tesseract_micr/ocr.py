import logging
import logging.config
import sys
import pytesseract;

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
        cfg = f""
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_string(path, lang='micr', config=cfg)
        logger.debug("-> "+res)
        return res


    def version(self):
        return pytesseract.get_tesseract_version()


