import pickle

def load_models():
    """
    
    """
    with open('webpage/artifacts/models/lgbm_base.pkl','rb') as handle:
        lgbm_model = pickle.load(handle)

    with open('webpage/artifacts/models/rf_base.pkl','rb') as handle:
        rf_model = pickle.load(handle)

    return lgbm_model, rf_model

def load_encoder():
    """
    dict_encoder: contendrá todos los encoders con sus respectivos nombres.
    """

    with open('webpage/artifacts/label_encoder_dict.pkl','rb') as handle:
        dict_encoder = pickle.load(handle)
    
    #Validar.

    return dict_encoder

def load_discretizer():

    with open('webpage/artifacts/discretizer.pkl','rb') as handle:
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