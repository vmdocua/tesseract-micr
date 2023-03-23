import logging
from datetime import datetime
import socket
import os

from flask import render_template, make_response, \
    jsonify, request, Markup, Blueprint

from docsultant.core import app_config

from docsultant.ocr import TesseractOcr
from docsultant.imgproc import ImageProcessor

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

def response_ok(res, mimetype):
    response = make_response(res, 200)
    response.mimetype = mimetype
    return response

@test_bp.route('/tesseract_version', methods=['GET', 'POST'])
def tesseract_version():
    logger.debug("tesseract_version")
    t = TesseractOcr()
    return response_ok(t.tesseract_version(), "text/plain")

@test_bp.route('/tesseract_plain', methods=['GET', 'POST'])
def tesseract_plain():
    logger.debug("tesseract_plain")
    path = request.form["path"]
    logger.debug(f"path={path}")
    chain = request.form["chain"]
    logger.debug(f"chain={chain}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.tesseract_plain(path2, chain)
    logger.debug(f"res={res}")
    return response_ok(res, "text/plain")

@test_bp.route('/tesseract_hocr', methods=['GET', 'POST'])
def tesseract_hocr():
    logger.debug("tesseract_hocr")
    path = request.form["path"]
    logger.debug(f"path={path}")
    chain = request.form["chain"]
    logger.debug(f"chain={chain}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.tesseract_hocr(path2, chain)
    res2 = "\n".join([line.text for line in res.lines])
    res2 = res2 + "\n\n##############################\n\n" + res.hocr
    #logger.debug(f"res={res}")
    return response_ok(res2, "application/x-view-source")

@test_bp.route('/tesseract_hocr_visualize', methods=['GET', 'POST'])
def tesseract_hocr_visualize():
    logger.debug("tesseract_hocr_visualize")
    path = request.form["path"]
    logger.debug(f"path={path}")
    chain = request.form["chain"]
    logger.debug(f"chain={chain}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    doc = t.tesseract_hocr(path2, chain)
    data = t.hocr_visualize_as_png(path2, chain, doc)
    return response_ok(data, "image/png")

@test_bp.route('/tesseract_micr', methods=['GET', 'POST'])
def tesseract_micr():
    logger.debug("tesseract_micr")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.tesseract_micr(path2)
    logger.debug(f"res={res}")
    return response_ok(res, "text/plain")

@test_bp.route('/tesseract_micr_hocr', methods=['GET', 'POST'])
def tesseract_micr_hocr():
    logger.debug("tesseract_micr_hocr")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.tesseract_micr_hocr(path2)
    res2 = "\n".join([line.text for line in res.lines])
    res2 = res2 + "\n\n##############################\n\n" + res.hocr
    #logger.debug(f"res={res}")
    return response_ok(res2, "application/x-view-source")

@test_bp.route('/ocr_check', methods=['GET', 'POST'])
def ocr_check():
    logger.debug("ocr_check")
    path = request.form["path"]
    logger.debug(f"path={path}")
    chain = request.form["chain"]
    logger.debug(f"chain={chain}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    logger.debug(f"path2={path2}")
    t = TesseractOcr()
    res = t.ocr_check(path2, chain)
    logger.debug(f"res={res}")
    return response_ok(res, "text/plain")

@test_bp.route('/imgproc_border', methods=['GET', 'POST'])
def imgproc_border():
    logger.debug("imgproc_border")
    path = request.form["path"]
    logger.debug(f"path={path}")
    width = int(request.form["width"])
    logger.debug(f"width={width}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.border(path2, width)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_bw', methods=['GET', 'POST'])
def imgproc_bw():
    logger.debug("imgproc_bw")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.bw(path2)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_invert', methods=['GET', 'POST'])
def imgproc_invert():
    logger.debug("imgproc_invert")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.invert(path2)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_scale', methods=['GET', 'POST'])
def imgproc_scale():
    logger.debug("imgproc_scale")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    factor = float(request.form["factor"])
    logger.debug(f"factor={factor}")
    p = ImageProcessor()
    data = p.scale(path2, factor)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_sharpen', methods=['GET', 'POST'])
def imgproc_sharpen():
    logger.debug("imgproc_sharpen")
    path = request.form["path"]
    logger.debug(f"path={path}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.sharpen(path2)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_rotate', methods=['GET', 'POST'])
def imgproc_rotate():
    logger.debug("imgproc_rotate")
    path = request.form["path"]
    angle = int(request.form["angle"])
    logger.debug(f"path={path}, angle={angle}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.rotate(path2, angle)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_threshold', methods=['GET', 'POST'])
def imgproc_threshold():
    logger.debug("imgproc_threshold")
    path = request.form["path"]
    threshold = int(request.form["threshold"])
    logger.debug(f"path={path}, threshold={threshold}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.threshold(path2, threshold)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/imgproc_chain', methods=['GET', 'POST'])
def imgproc_chain():
    logger.debug("imgproc_chain")
    path = request.form["path"]
    commands = request.form["commands"]
    logger.debug(f"path={path}, commands={commands}")
    path2 = os.path.join(app_config.ROOT_PATH, path);
    p = ImageProcessor()
    data = p.chain(path2, commands)
    return response_ok(data, p.OUT_MIME_TYPE)

@test_bp.route('/vips_version', methods=['GET', 'POST'])
def vips_version():
    logger.debug("vips_version")
    p = ImageProcessor()
    return response_ok(p.vips_version(), "text/plain")

@test_bp.route('/box_scale', methods=['GET', 'POST'])
def box_scale():
    logger.debug("box_scale")
    #
    path_in = request.form["pathIn"]
    logger.debug(f"path_in={path_in}")
    path_in2 = os.path.join(app_config.ROOT_PATH, path_in);
    logger.debug(f"path_in2={path_in2}")
    #
    path_out = request.form["pathOut"]
    logger.debug(f"path_out={path_out}")
    path_out2 = os.path.join(app_config.ROOT_PATH, path_out);
    logger.debug(f"path_out2={path_out2}")
    #
    scale = float(request.form["scale"])
    logger.debug(f"scale={scale}")
    #
    t = TesseractOcr()
    res = t.box_scale(path_in2, path_out2, scale)
    logger.debug(f"res={res}")
    return response_ok(res, "text/plain")

@test_bp.route('/generate_box_image', methods=['GET', 'POST'])
def generate_box_image():
    logger.debug("generate_box_image")
    #
    path_font = request.form["pathFont"]
    logger.debug(f"path_font={path_font}")
    path_font2 = os.path.join(app_config.ROOT_PATH, path_font);
    logger.debug(f"path_font2={path_font2}")
    #
    font_size = int(request.form["fontSize"])
    logger.debug(f"font_size={font_size}")
    #
    font_mode = request.form["fontMode"]
    logger.debug(f"font_mode={font_mode}")
    #
    path_gt = request.form["pathGt"]
    logger.debug(f"path_gt={path_gt}")
    path_gt2 = os.path.join(app_config.ROOT_PATH, path_gt);
    logger.debug(f"path_gt2={path_gt2}")
    #
    path_tif = request.form["pathTif"]
    logger.debug(f"path_tif={path_tif}")
    path_tif2 = os.path.join(app_config.ROOT_PATH, path_tif);
    logger.debug(f"path_tif2={path_tif2}")
    #
    path_box = request.form["pathBox"]
    logger.debug(f"path_box={path_box}")
    path_box2 = os.path.join(app_config.ROOT_PATH, path_box);
    logger.debug(f"path_box2={path_box2}")
    #
    scale = int(request.form["scale"])
    logger.debug(f"scale={scale}")
    #
    t = TesseractOcr()
    res = t.generate_box_image(path_font2, font_size, font_mode, path_gt2, path_tif2, path_box2, scale)
    logger.debug(f"res={res}")
    return response_ok(res, "text/plain")
