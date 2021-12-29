from app import create_app
from app.utils import load_models

model_dict = load_models()

app = create_app(model_dict)