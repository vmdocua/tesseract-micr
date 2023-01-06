import logging
import logging.config
import sys
import pytesseract;

logger = logging.getLogger(__name__)

class TesseractOcr:

    def __int__(self):
        pass

    def version(self):
        return pytesseract.get_tesseract_version()


