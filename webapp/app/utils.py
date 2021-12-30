import pickle
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.join(BASE_DIR, 'artifacts'),'models')
ARTIFACTS_DIR = os.path.join(BASE_DIR,'artifacts')

def load_models():
    """LOAD MODELS FROM MODELS FILE
    """
    MODELS_LIST = ['lgbm_base','rf_base']
    model_dict = dict()

    for model in MODELS_LIST:
        
        with open(os.path.join(MODELS_DIR, model + '.pkl'), 'rb') as handle:
            model_dict[model] = pickle.load(handle)
        
    return model_dict

def load_encoder():
    """
    dict_encoder: contendrá todos los encoders con sus respectivos nombres.
    """

    ENCODER_NAME = 'label_encoder_dict'
    with open(os.path.join(ARTIFACTS_DIR, ENCODER_NAME + '.pkl'), 'rb') as handle:
        dict_encoder = pickle.load(handle)

    return dict_encoder

def load_discretizer():

    DISCRETIZER_NAME = 'discretizer'
    

    with open(os.path.join(ARTIFACTS_DIR, DISCRETIZER_NAME + '.pkl'), 'rb') as handle:
        discretizer = pickle.load(handle)
    #Validate
        return discretizer

def dict_encoder_classes():
    """
    Siempre usaremos el encoder en .pkl porque puede haber casos en los que 
    tendremos que cambiar el diccionario. Por eso será dinámico.
    
    Returns a dictionary with {name_class1: [val1, val2, ..., valn],
                            name_class2: [val1, val2, ..., valn]}
    """

    dict_encoder = load_encoder()

    dict_list_classes = {name_encoder: encoder_.classes_.tolist() for name_encoder, encoder_ in dict_encoder.items()}
        
    return dict_list_classes