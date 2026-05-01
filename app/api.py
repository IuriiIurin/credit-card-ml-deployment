# Веб-сервис с двумя эндпоинтами:
# /health (GET) - возвращает 'OK', если все нормально
# /predict (POST) - принимает JSON с признаками клиента, прогоняет через модель и возвращает предсказание (0/1), вероятность дефолта и версию модели

from flask import Flask, request, jsonify
from model_handler import load_model
import numpy as np

app = Flask(__name__)

model = load_model()  # загружаем модель при старте сервера

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'}), 200  # проверка работоспособности сервиса

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()                                                # получаем JSON
        features = np.array([data[key] for key in sorted(data.keys())]).reshape(1, -1)  # формируем массив признаков
        prediction = model.predict(features)                                    # предсказание класса
        probability = model.predict_proba(features)[0][1]                       # вероятность дефолта
        return jsonify({
            'prediction': int(prediction[0]),                                   # 0 или 1
            'probability': float(probability),                                  # вероятность дефолта
            'model_version': 'v1'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400                                  # возвращаем ошибку

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)