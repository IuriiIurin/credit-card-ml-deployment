# Веб-сервис с двумя эндпоинтами:
# /health (GET) - возвращает 'OK', если все нормально
# /predict (POST) - принимает JSON с признаками клиента, прогоняет через модель и возвращает предсказание (0/1), вероятность дефолта и версию модели

from flask import Flask, request, jsonify
from model_handler import load_model
import numpy as np
import logging
import json
import os

FEATURE_COLUMNS = ['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
                   'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
                   'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
                   'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

# настройка логирования
os.makedirs('logs', exist_ok=True)                                                  # создаём папку logs если её нет
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

app = Flask(__name__)

model_v1 = load_model('models/model_v1.pkl')                                        # загружаем модель v1
model_v2 = load_model('models/model_v2.pkl')                                        # загружаем модель v2

models = {'v1': model_v1, 'v2': model_v2}                                           # словарь моделей

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:              
        
        data = request.get_json()
        version = data.pop('model_version', 'v1')  # убираем из признаков
        user_id = data.pop('user_id', None)        # убираем из признаков, сохраняем для лога
        model = models.get(version)

        if model is None:
            return jsonify({'error': f'версия {version} не найдена'}), 400

        features = np.array([data[key] for key in FEATURE_COLUMNS]).reshape(1, -1)  # теперь model_version уже убран
        prediction = model.predict(features)
        probability = model.predict_proba(features)[0][1]

        logging.info(json.dumps({
            'user_id': user_id,
            'input': data,
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'model_version': version
        }))                                                                         # логируем запрос и ответ

        return jsonify({
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'model_version': version
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)