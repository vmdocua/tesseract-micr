import logging
import logging.config
import sys
import platform
from io import StringIO
import urllib.request
import base64
from pathlib import Path
from tesseract_micr.config import AppConfig

logger = logging.getLogger(__name__)

app_config = AppConfig()

class NamedStringIO(StringIO):

    def __init__(self, name, content):
        super(NamedStringIO, self).__init__(content)
        self._name = name


    def __str__(self):
        return self._name

def _config_request(url):
    req = urllib.request.Request(url)
    if app_config.CONFIG_SERVER_USER is not None:
        s1 = base64.b64encode(bytes(f"{app_config.CONFIG_SERVER_USER}:{app_config.CONFIG_SERVER_PASSWORD}", 'ascii'))
        req.add_header("Authorization", "Basic %s" % s1.decode('utf-8'))
    return req

def app_init():

    if app_config.initialized():
        logger.info("Application already initialized")
        return


    LOGGING_INI = 'logging.ini'
    logFiles = [
        app_config.SECURE_CONFIG_PATH + '/' + LOGGING_INI,
        app_config.HOST_CONFIG_PATH + '/' + LOGGING_INI,
        app_config.ROOT_PATH + '/' + LOGGING_INI
    ]

    for logFile in logFiles:
        if hasattr(logFile, 'readline') or Path(logFile).exists():
            logging.config.fileConfig(logFile, disable_existing_loggers=False)
            logger.info("Found logger configuration file: "+str(logFile))
            break

    logger.info("Application init...")

    logger.info('[Platform Info]: ')
    logger.info(' system    : ' + platform.system())
    logger.info(' node      : ' + platform.node())
    logger.info(' release   : ' + platform.release())
    logger.info(' version   : ' + platform.version())
    logger.info(' machine   : ' + platform.machine())
    logger.info(' processor : ' + platform.processor())
    logger.info(' python    : ' + '.'.join(map(str, sys.version_info)) + ', ' + sys.executable)

    # load configuration from multiple INI files and merge
    TESSERACT_MICR_INI = 'tesseract_micr.ini'
    iniPaths = [
        app_config.ROOT_PATH + '/' + TESSERACT_MICR_INI,
        app_config.HOST_CONFIG_PATH + '/' + TESSERACT_MICR_INI,
        app_config.SECURE_CONFIG_PATH + '/' + TESSERACT_MICR_INI
    ]

    iniFiles = None


    app_config.load(iniPaths, iniFiles);

    logger.info('Environment: '+app_config.ENV)
    logger.info("Application initialized successfully");
