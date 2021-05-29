import pickle

def load_models():
    """
    TO DO: Sistematizar el path de los modelos.
    """
    with open('artifacts/models/lgbm_base.pkl','rb') as handle:
        lgbm_model = pickle.load(handle)

    with open('artifacts/models/rf_base.pkl','rb') as handle:
        rf_model = pickle.load(handle)

    return lgbm_model, rf_model

def load_encoder():
    """
    dict_encoder: contendrá todos los encoders con sus respectivos nombres.
    """

    with open('artifacts/label_encoder_dict.pkl','rb') as handle:
        dict_encoder = pickle.load(handle)
    
    #Validar.

    return dict_encoder

def load_discretizer():

    with open('artifacts/discretizer.pkl','rb') as handle:
        discretizer = pickle.load(handle)
    #Validate
        return discretizer

def number_to_class(number, dict_encoder, column = 'Area_constr_cat'):
    """
    Tomará los valores que tiene dict_encoder para poder categorizar el valor de una columna
    en las categorías ya dadas por este encoder.
    """
    categorias = dict_encoder[column].classes_


    return 0