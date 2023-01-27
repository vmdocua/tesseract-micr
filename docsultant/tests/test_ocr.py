import pytest
from docsultant.ocr import TesseractOcr

def test_tesseract_version():
    t = TesseractOcr()
    s = t.tesseract_version()
    print(" version={}".format(s))
    v = s.split(" ")[1]
    assert v.startswith("5.") or v.startswith("4."), \
        "Unsupported tesseract version {}".format(s)
