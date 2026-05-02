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