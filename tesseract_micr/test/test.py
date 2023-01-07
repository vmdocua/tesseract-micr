import logging
from datetime import datetime
import socket

from flask import render_template, make_response, \
    jsonify, request, Markup, Blueprint

from tesseract_micr.core import app_config

from tesseract_micr.ocr import TesseractOcr

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

test_bp = Blueprint('test_bp', __name__)



@test_bp.route('/')
def home():
    logger.debug("home")
    return render_template('test/home.j2', name1='Flask')


@test_bp.route('/hw', methods=['GET', 'POST'])
def hw():
    logger.debug("hw")
    return Markup('<h3>Hello World!!!</h3>')


@test_bp.route('/ping', methods=['GET', 'POST'])
def ping():
    logger.debug("ping")
    res = {}
    headers = { "Content-Type" : "application/json" }
    res["message"] = f'pong: {str(request.form.get("text1"))}'
    res["success"] = True
    res["host"] = socket.gethostname()
    res["ts"] = str(datetime.now())
    return make_response(jsonify(res), 200, headers)


@test_bp.route('/tesseract_version', methods=['GET', 'POST'])
def tesseract_version():
    logger.debug("tesseract_version")
    t = TesseractOcr()
    return Markup(t.version())

@test_bp.route('/ocr_plain', methods=['GET', 'POST'])
def ocr_plain():
    logger.debug("ocr_plain")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = app_config.ROOT_PATH + "/" + path
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.ocrPlain(path2)
    logger.debug(f"res={res}")
    return Markup(res)

@test_bp.route('/ocr_micr', methods=['GET', 'POST'])
def ocr_micr():
    logger.debug("ocr_micr")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = app_config.ROOT_PATH + "/" + path
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.ocrMicr(path2)
    logger.debug(f"res={res}")
    return Markup(res)
