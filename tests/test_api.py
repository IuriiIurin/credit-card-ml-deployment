import requests
import hashlib
import pandas as pd
import random

BASE_URL = 'http://localhost:5000'

FEATURE_COLUMNS = ['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
                   'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
                   'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
                   'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

df = pd.read_csv('data/UCI_Credit_Card.csv')                            # читаем датасет

def get_random_client():
    row = df.sample(1).iloc[0]                                          # берём случайную строку
    return {col: row[col] for col in FEATURE_COLUMNS}                   # возвращаем только признаки

def stable_hash(user_id):
    return int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)      # стабильный хэш

def get_version(user_id):
    bucket = stable_hash(user_id) % 100                                 # число от 0 до 99
    return "v1" if bucket < 50 else "v2"                                # разбиение 50/50

# Проверка запущенности сервиса
def test_health():
    r = requests.get(f'{BASE_URL}/health')
    if r.status_code == 200 and r.json()['status'] == 'OK':
        print(f'Проверка работы: {r.json()['status']}')
    else:
        print(f'Ошибка: {r.status_code} {r.json()}')

def test_predict_v1():
    data = {**get_random_client(), "model_version": "v1"}
    r = requests.post(f'{BASE_URL}/predict', json=data)
    if r.status_code == 200 and r.json()['model_version'] == 'v1' and r.json()['prediction'] in [0, 1]:
        print('test_predict_v1: OK')
    else:
        print(f'test_predict_v1 FAIL : {r.json()}')

def test_predict_v2():
    data = {**get_random_client(), "model_version": "v2"}
    r = requests.post(f'{BASE_URL}/predict', json=data)
    if r.status_code == 200 and r.json()['model_version'] == 'v2' and r.json()['prediction'] in [0, 1]:
        print('test_predict_v2: OK')
    else:
        print(f'test_predict_v2 FAIL : {r.json()}')

def test_invalid_request():
    r = requests.post(f'{BASE_URL}/predict', json={"invalid": "data"})
    if r.status_code == 400:
        print('Проверка ошибочного запроса: OK')
    else:
        print(f'Проверка ошибочного запроса неудачна: {r.status_code}')

def test_ab_routing():
    for user_id in range(10):                                           # проверяем 10 пользователей
        version = get_version(user_id)
        data = {**get_random_client(), "user_id": user_id, "model_version": version}
        r = requests.post(f'{BASE_URL}/predict', json=data)
        if r.status_code == 200 and r.json()['model_version'] == version:
            print(f'test_ab_routing user_id={user_id} version={version}: OK')
        else:
            print(f'test_ab_routing user_id={user_id}: FAIL - {r.json()}')

if __name__ == '__main__':
    test_health()
    test_predict_v1()
    test_predict_v2()
    test_invalid_request()
    test_ab_routing()
    print('Все тесты завершены!')