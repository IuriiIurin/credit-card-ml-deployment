## Credit Card Default Prediction Service
Сессионная работа Юрина Юрия (Iurii Iurin, М255809), по предмету"Внедрение моделей ML"

## Описание проекта

Сервис машинного обучения для прогнозирования дефолта по кредитным картам.
Разработан в рамках учебного проекта по курсу "Внедрение моделей ML".

Домен: финансы / кредитный скоринг.
Датасет: UCI Credit Card Default Dataset (30000 клиентов, Тайвань, 2005).
Задача: бинарная классификация, предсказать дефолт клиента в следующем месяце (0/1).

## Стек технологий

Python, Flask, scikit-learn, Docker, Docker Compose

## Возможности сервиса

- Предсказание дефолта по кредитной карте через REST API
- Поддержка двух версий модели (v1/v2) для A/B тестирования
- Логирование всех запросов и ответов в формате JSON

## Запуск проекта

### Локально

1. Клонировать репозиторий:
```bash
git clone https://github.com/iuriiiurin/credit-card-ml-deployment
```

2. Создать и активировать окружение:
```powershell
py -3.12 -m venv project_venv
.\project_venv\Scripts\Activate.ps1
```

3. Установить зависимости:
```powershell
pip install -r requirements.txt
```

4. Обучить модель:
```powershell
python models/train_model.py
```

5. Запустить сервис:
```powershell
python app/api.py
```

### В Docker

1. Собрать образ:
```powershell
docker build -t iuriiiurin/credit-card-ml -f docker/Dockerfile .
```

2. Запустить контейнер:
```powershell
docker run -d --rm --name=credit-card-ml -p 5000:5000 iuriiiurin/credit-card-ml
```

### Через Docker Compose
```powershell
docker-compose up --build
```

### Скачать готовый образ с Docker Hub
```powershell
docker pull iuriiiurin/credit-card-ml
docker run -d --rm --name=credit-card-ml -p 5000:5000 iuriiiurin/credit-card-ml
```

## Примеры запросов к API

### Проверка работоспособности (GET /health)
```bash
curl http://localhost:5000/health
```

Ответ:
```json
{"status": "OK"}
```

Чтобы логи попадали из контенйреа в локальную папку:
```powershell
docker run -d --rm --name=credit-card-ml -p 5000:5000 -v ${PWD}/logs:/app/logs iuriiiurin/credit-card-ml
```

### Предсказание дефолта (POST /predict)

Модель v1 (LogisticRegression):
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"LIMIT_BAL": 20000, "SEX": 2, "EDUCATION": 2, "MARRIAGE": 1, "AGE": 24, "PAY_0": 2,"PAY_2": 2, "PAY_3": -1, "PAY_4": -1, "PAY_5": -2, "PAY_6": -2, "BILL_AMT1": 3913, "BILL_AMT2": 3102, "BILL_AMT3": 689, "BILL_AMT4": 0, "BILL_AMT5": 0, "BILL_AMT6": 0, "PAY_AMT1": 0, "PAY_AMT2": 689, "PAY_AMT3": 0, "PAY_AMT4": 0, "PAY_AMT5": 0, "PAY_AMT6": 0, "model_version": "v1"}'
```

Ответ:
```json
{"model_version": "v1", "prediction": 1, "probability": 0.77}
```

Модель v2 (RandomForestClassifier), передать "model_version": "v2" вместо "v1" (в конце строки запроса):
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"LIMIT_BAL": 20000, "SEX": 2, "EDUCATION": 2, "MARRIAGE": 1, "AGE": 24, "PAY_0": 2,"PAY_2": 2, "PAY_3": -1, "PAY_4": -1, "PAY_5": -2, "PAY_6": -2, "BILL_AMT1": 3913, "BILL_AMT2": 3102, "BILL_AMT3": 689, "BILL_AMT4": 0, "BILL_AMT5": 0, "BILL_AMT6": 0, "PAY_AMT1": 0, "PAY_AMT2": 689, "PAY_AMT3": 0, "PAY_AMT4": 0, "PAY_AMT5": 0, "PAY_AMT6": 0, "model_version": "v2"}'
```

Ответ:
```json
{"model_version": "v2", "prediction": 1, "probability": 0.84}
```

## Формат запросов и ответов

### POST /predict

Запрос - JSON объект со следующими полями:
- LIMIT_BAL (float)             - кредитный лимит в NT долларах
- SEX (int)                     - пол (1 = мужской, 2 = женский)
- EDUCATION (int)               - образование (1 = аспирантура, 2 = университет, 3 = школа, 4 = другое)
- MARRIAGE (int)                - семейное положение (1 = женат/замужем, 2 = холост/не замужем, 3 = другое)
- AGE (int)                     - возраст в годах
- PAY_0..PAY_6 (int)            - статус оплаты за каждый месяц (-2,-1=вовремя, 1-9 = просрочка в месяцах)
- BILL_AMT1 - BILL_AMT6 (float) - сумма счета за каждый месяц в NT долларах
- PAY_AMT1 - PAY_AMT6 (float)   - сумма предыдущего платежа за каждый месяц
- model_version (str)           - версия модели "v1" или "v2", по умолчанию "v1"

Ответ:
- prediction (int)              - предсказание дефолта (0 = нет, 1 = да)
- probability (float)           - вероятность дефолта от 0.0 до 1.0
- model_version (str)           - версия модели использованная для предсказания

Ошибки:
- 400 - невалидный JSON или отсутствующие поля

## Ссылка на Docker Hub

Образ доступен по адресу: https://hub.docker.com/r/iuriiiurin/credit-card-ml

Скачать образ:
```powershell
docker pull iuriiiurin/credit-card-ml
```

## Структура репозитория
```
app/                        - код Flask сервиса
    __init__.py             - инициализация модуля
    api.py                  - Flask приложение с эндпоинтами /health и /predict
    model_handler.py        - загрузка модели для инференса
models/                     - модели и скрипт обучения
    train_model.py          - скрипт обучения и сохранения моделей
    model_v1.pkl            - обученная модель LogisticRegression
    model_v2.pkl            - обученная модель RandomForestClassifier
tests/                      - тесты
    test_api.py             - тесты эндпоинтов и A/B маршрутизации
docker/                     - конфигурация Docker
    Dockerfile              - сборка образа сервиса
data/                       - датасет (не включён в репозиторий)
notebooks/                  - jupyter ноутбуки
    EDA.ipynb               - разведочный анализ данных и обоснование модели
requirements.txt            - зависимости Python
docker-compose.yml          - оркестрация сервиса
ab_test_plan.md             - план A/B тестирования
ARCHITECTURE.md             - описание архитектуры сервиса
README.md                   - документация проекта
```

## Примеры логов
```
2026-05-02 17:18:33,056 172.17.0.1 - - [02/May/2026 17:18:33] "GET /health HTTP/1.1" 200 -
2026-05-02 17:18:33,071 {"user_id": null, "input": {"LIMIT_BAL": 80000.0, "SEX": 2.0, "EDUCATION": 3.0, "MARRIAGE": 1.0, "AGE": 55.0, "PAY_0": 2.0, "PAY_2": 2.0, "PAY_3": 0.0, "PAY_4": 0.0, "PAY_5": 0.0, "PAY_6": 0.0, "BILL_AMT1": 71905.0, "BILL_AMT2": 70150.0, "BILL_AMT3": 72017.0, "BILL_AMT4": 73816.0, "BILL_AMT5": 75584.0, "BILL_AMT6": 77365.0, "PAY_AMT1": 0.0, "PAY_AMT2": 3000.0, "PAY_AMT3": 3000.0, "PAY_AMT4": 3000.0, "PAY_AMT5": 3000.0, "PAY_AMT6": 3000.0}, "prediction": 1, "probability": 0.7895396884936117, "model_version": "v1"}
2026-05-02 17:18:33,071 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,098 {"user_id": null, "input": {"LIMIT_BAL": 500000.0, "SEX": 2.0, "EDUCATION": 1.0, "MARRIAGE": 2.0, "AGE": 34.0, "PAY_0": -2.0, "PAY_2": -2.0, "PAY_3": -2.0, "PAY_4": -2.0, "PAY_5": -2.0, "PAY_6": -2.0, "BILL_AMT1": 11765.0, "BILL_AMT2": 6599.0, "BILL_AMT3": 11421.0, "BILL_AMT4": -83.0, "BILL_AMT5": 49699.0, "BILL_AMT6": 3821.0, "PAY_AMT1": 6648.0, "PAY_AMT2": 11986.0, "PAY_AMT3": 0.0, "PAY_AMT4": 49947.0, "PAY_AMT5": 3840.0, "PAY_AMT6": 11939.0}, "prediction": 0, "probability": 0.02, "model_version": "v2"}
2026-05-02 17:18:33,099 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,106 172.17.0.1 - - [02/May/2026 17:18:33] "[31m[1mPOST /predict HTTP/1.1[0m" 400 -
2026-05-02 17:18:33,127 {"user_id": 0, "input": {"LIMIT_BAL": 30000.0, "SEX": 2.0, "EDUCATION": 3.0, "MARRIAGE": 1.0, "AGE": 31.0, "PAY_0": 0.0, "PAY_2": 0.0, "PAY_3": 0.0, "PAY_4": 0.0, "PAY_5": 0.0, "PAY_6": 0.0, "BILL_AMT1": 9388.0, "BILL_AMT2": 10387.0, "BILL_AMT3": 10624.0, "BILL_AMT4": 11539.0, "BILL_AMT5": 11771.0, "BILL_AMT6": 9075.0, "PAY_AMT1": 1162.0, "PAY_AMT2": 1229.0, "PAY_AMT3": 1144.0, "PAY_AMT4": 376.0, "PAY_AMT5": 329.0, "PAY_AMT6": 345.0}, "prediction": 0, "probability": 0.1, "model_version": "v2"}
2026-05-02 17:18:33,128 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,137 {"user_id": 1, "input": {"LIMIT_BAL": 160000.0, "SEX": 1.0, "EDUCATION": 2.0, "MARRIAGE": 2.0, "AGE": 31.0, "PAY_0": 0.0, "PAY_2": 0.0, "PAY_3": 0.0, "PAY_4": 0.0, "PAY_5": 0.0, "PAY_6": 0.0, "BILL_AMT1": 24645.0, "BILL_AMT2": 24956.0, "BILL_AMT3": 25819.0, "BILL_AMT4": 25754.0, "BILL_AMT5": 25898.0, "BILL_AMT6": 25925.0, "PAY_AMT1": 1420.0, "PAY_AMT2": 1699.0, "PAY_AMT3": 1050.0, "PAY_AMT4": 1104.0, "PAY_AMT5": 1041.0, "PAY_AMT6": 1000.0}, "prediction": 0, "probability": 0.4923415606166762, "model_version": "v1"}
2026-05-02 17:18:33,138 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,148 {"user_id": 2, "input": {"LIMIT_BAL": 490000.0, "SEX": 2.0, "EDUCATION": 2.0, "MARRIAGE": 1.0, "AGE": 42.0, "PAY_0": -1.0, "PAY_2": -1.0, "PAY_3": -1.0, "PAY_4": 0.0, "PAY_5": -1.0, "PAY_6": -1.0, "BILL_AMT1": 15838.0, "BILL_AMT2": 11356.0, "BILL_AMT3": 25409.0, "BILL_AMT4": 15926.0, "BILL_AMT5": 8604.0, "BILL_AMT6": 8941.0, "PAY_AMT1": 11404.0, "PAY_AMT2": 25458.0, "PAY_AMT3": 86.0, "PAY_AMT4": 8711.0, "PAY_AMT5": 5034.0, "PAY_AMT6": 1345.0}, "prediction": 0, "probability": 0.2359248405973999, "model_version": "v1"}
2026-05-02 17:18:33,148 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,172 {"user_id": 3, "input": {"LIMIT_BAL": 210000.0, "SEX": 1.0, "EDUCATION": 3.0, "MARRIAGE": 2.0, "AGE": 28.0, "PAY_0": 0.0, "PAY_2": 0.0, "PAY_3": 0.0, "PAY_4": 0.0, "PAY_5": 0.0, "PAY_6": 0.0, "BILL_AMT1": 58340.0, "BILL_AMT2": 58644.0, "BILL_AMT3": 59855.0, "BILL_AMT4": 61013.0, "BILL_AMT5": 61097.0, "BILL_AMT6": 65089.0, "PAY_AMT1": 2107.0, "PAY_AMT2": 3000.0, "PAY_AMT3": 3000.0, "PAY_AMT4": 2500.0, "PAY_AMT5": 6000.0, "PAY_AMT6": 8000.0}, "prediction": 0, "probability": 0.02, "model_version": "v2"}
2026-05-02 17:18:33,173 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,181 {"user_id": 4, "input": {"LIMIT_BAL": 30000.0, "SEX": 2.0, "EDUCATION": 2.0, "MARRIAGE": 1.0, "AGE": 33.0, "PAY_0": 0.0, "PAY_2": 0.0, "PAY_3": -1.0, "PAY_4": 0.0, "PAY_5": 0.0, "PAY_6": 0.0, "BILL_AMT1": 4101.0, "BILL_AMT2": 157.0, "BILL_AMT3": 30321.0, "BILL_AMT4": 29225.0, "BILL_AMT5": 29575.0, "BILL_AMT6": 28850.0, "PAY_AMT1": 172.0, "PAY_AMT2": 33635.0, "PAY_AMT3": 1368.0, "PAY_AMT4": 1108.0, "PAY_AMT5": 958.0, "PAY_AMT6": 1353.0}, "prediction": 0, "probability": 0.4620915059107191, "model_version": "v1"}
2026-05-02 17:18:33,183 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,204 {"user_id": 5, "input": {"LIMIT_BAL": 360000.0, "SEX": 1.0, "EDUCATION": 1.0, "MARRIAGE": 1.0, "AGE": 40.0, "PAY_0": 0.0, "PAY_2": 0.0, "PAY_3": 2.0, "PAY_4": -1.0, "PAY_5": -1.0, "PAY_6": -1.0, "BILL_AMT1": 76584.0, "BILL_AMT2": 85400.0, "BILL_AMT3": 17295.0, "BILL_AMT4": 8331.0, "BILL_AMT5": 2643.0, "BILL_AMT6": 6008.0, "PAY_AMT1": 21358.0, "PAY_AMT2": 86.0, "PAY_AMT3": 8372.0, "PAY_AMT4": 2656.0, "PAY_AMT5": 6038.0, "PAY_AMT6": 3325.0}, "prediction": 0, "probability": 0.12, "model_version": "v2"}
2026-05-02 17:18:33,207 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,219 {"user_id": 6, "input": {"LIMIT_BAL": 330000.0, "SEX": 1.0, "EDUCATION": 1.0, "MARRIAGE": 2.0, "AGE": 34.0, "PAY_0": -1.0, "PAY_2": -1.0, "PAY_3": -1.0, "PAY_4": -1.0, "PAY_5": 0.0, "PAY_6": -1.0, "BILL_AMT1": 316.0, "BILL_AMT2": 310.0, "BILL_AMT3": 6994.0, "BILL_AMT4": 632.0, "BILL_AMT5": 316.0, "BILL_AMT6": 38277.0, "PAY_AMT1": 310.0, "PAY_AMT2": 7006.0, "PAY_AMT3": 2000.0, "PAY_AMT4": 0.0, "PAY_AMT5": 38277.0, "PAY_AMT6": 6000.0}, "prediction": 0, "probability": 0.3099275634881951, "model_version": "v1"}
2026-05-02 17:18:33,219 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,240 {"user_id": 7, "input": {"LIMIT_BAL": 30000.0, "SEX": 2.0, "EDUCATION": 1.0, "MARRIAGE": 1.0, "AGE": 30.0, "PAY_0": 0.0, "PAY_2": 0.0, "PAY_3": 2.0, "PAY_4": 2.0, "PAY_5": 0.0, "PAY_6": 0.0, "BILL_AMT1": 15199.0, "BILL_AMT2": 17728.0, "BILL_AMT3": 19129.0, "BILL_AMT4": 18527.0, "BILL_AMT5": 18758.0, "BILL_AMT6": 19285.0, "PAY_AMT1": 3100.0, "PAY_AMT2": 2000.0, "PAY_AMT3": 0.0, "PAY_AMT4": 679.0, "PAY_AMT5": 837.0, "PAY_AMT6": 721.0}, "prediction": 1, "probability": 0.8, "model_version": "v2"}
2026-05-02 17:18:33,240 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,248 {"user_id": 8, "input": {"LIMIT_BAL": 30000.0, "SEX": 2.0, "EDUCATION": 2.0, "MARRIAGE": 2.0, "AGE": 27.0, "PAY_0": 2.0, "PAY_2": 2.0, "PAY_3": 2.0, "PAY_4": 2.0, "PAY_5": 2.0, "PAY_6": 2.0, "BILL_AMT1": 15191.0, "BILL_AMT2": 16144.0, "BILL_AMT3": 16383.0, "BILL_AMT4": 16518.0, "BILL_AMT5": 16907.0, "BILL_AMT6": 17279.0, "PAY_AMT1": 1500.0, "PAY_AMT2": 800.0, "PAY_AMT3": 700.0, "PAY_AMT4": 800.0, "PAY_AMT5": 800.0, "PAY_AMT6": 800.0}, "prediction": 1, "probability": 0.7975026439234819, "model_version": "v1"}
2026-05-02 17:18:33,248 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -
2026-05-02 17:18:33,268 {"user_id": 9, "input": {"LIMIT_BAL": 50000.0, "SEX": 2.0, "EDUCATION": 1.0, "MARRIAGE": 2.0, "AGE": 34.0, "PAY_0": 1.0, "PAY_2": -2.0, "PAY_3": -2.0, "PAY_4": -2.0, "PAY_5": -2.0, "PAY_6": -2.0, "BILL_AMT1": 0.0, "BILL_AMT2": 0.0, "BILL_AMT3": 0.0, "BILL_AMT4": 0.0, "BILL_AMT5": 300.0, "BILL_AMT6": 150.0, "PAY_AMT1": 0.0, "PAY_AMT2": 0.0, "PAY_AMT3": 0.0, "PAY_AMT4": 300.0, "PAY_AMT5": 0.0, "PAY_AMT6": 980.0}, "prediction": 0, "probability": 0.2, "model_version": "v2"}
2026-05-02 17:18:33,269 172.17.0.1 - - [02/May/2026 17:18:33] "POST /predict HTTP/1.1" 200 -

```
