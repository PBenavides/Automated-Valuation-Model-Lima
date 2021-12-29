from flask import Flask
from config import Config
from app.utils import load_models, load_discretizer, load_encoder

def create_app(model_dict, config_obj = Config):
    """
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)
    app.config['model_dict'] = model_dict
    
    print('IMPORTANDO ARTIFACTS')

    #app.discretizer = load_discretizer()
    #app.load_encoder = load_encoder()

    print('ARTIFACTS ------- DONE')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    print('main registrado')

    from app.inference import bp as inference_bp
    app.register_blueprint(inference_bp)
    print('inference registrado')
    app.app_context().push()

    print('ITS ALL DONE')
    return app

from app import utils