import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config


"""----------------- Logging -----------------"""
logging.basicConfig(level=logging.INFO)

file_log_handler = RotatingFileHandler("log.logs", maxBytes=1024*1024*100)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

file_log_handler.setFormatter(formatter)

logging.getLogger().addHandler(file_log_handler)


def create_app(model_dict, config_obj = Config):
    """model_dict: an object to load once the app is created.
    config_obj: Basic Config Object.
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)
    app.config['model_dict'] = model_dict
    

    app.logger.debug('already imported models')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.logger.debug('main bluerpint registered')

    from app.inference import bp as inference_bp
    app.register_blueprint(inference_bp)
    app.logger.debug('inference blueprint registered')
    app.app_context().push()

    return app

from app import utils