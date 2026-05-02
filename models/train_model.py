import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42

# Загрузка данных
df = pd.read_csv('data/UCI_Credit_Card.csv')            # путь относительно папки models

# Предобработка
df = df.drop(columns=['ID'])                            # удаляем ID
df['EDUCATION'] = df['EDUCATION'].replace(0, 4)         # исправляем аномалии
df['MARRIAGE'] = df['MARRIAGE'].replace(0, 3)           # исправляем аномалии

X = df.drop(columns=['default.payment.next.month'])     # признаки
y = df['default.payment.next.month']                    # таргет

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

# Обучение Логистической регрессии (первая модель)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=RANDOM_STATE))
])
pipeline.fit(X_train, y_train)

# Сохранение модели
with open('models/model_v1.pkl', 'wb') as f:
    pickle.dump(pipeline, f)                            # сохраняем pipeline

print('Модель сохранена в models/model_v1.pkl')

#  Обучение Случайного леса (вторая модель)
pipeline_v2 = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=RANDOM_STATE))
])
pipeline_v2.fit(X_train, y_train)

# Сохранение второй модели
with open('models/model_v2.pkl', 'wb') as f:
    pickle.dump(pipeline_v2, f)                         # сохраняем вторую модель

print('Модель v2 сохранена в models/model_v2.pkl')