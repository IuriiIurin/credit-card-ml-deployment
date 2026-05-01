# Функция загрузки модели для инференса

import pickle

def load_model(model_path='models/model_v1.pkl'):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)  
    return model