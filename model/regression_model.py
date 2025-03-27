# model/regression_model.py
import pickle

import numpy as np

from model.utils import get_df_houses_data, save_schema

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import OneHotEncoder

from sklearn.linear_model import LinearRegression



def train_and_save_model():
    """
    Entrena un modelo de regresión lineal para predecir precios de casas y guarda el modelo entrenado.
    
    Este proceso incluye:
    1. Carga de datos desde PostgreSQL
    2. Limpieza y preparación de datos (eliminación de columnas, manejo de duplicados)
    3. Feature engineering (creación de variables derivadas)
    4. Transformación de variables categóricas
    5. Entrenamiento de un modelo de regresión lineal
    6. Evaluación del rendimiento del modelo
    7. Persistencia del esquema de datos y del modelo entrenado
    
    Los precios son transformados a escala logarítmica para mejorar la distribución.
    
    Outputs:
    - Imprime métricas R² en conjuntos de entrenamiento y prueba
    - Guarda el esquema de datos en "artifacts/input_schema_predict_v0.1.0.json"
    - Guarda el modelo entrenado en "artifacts/modelo_lineal_v0.1.0.pkl"
    """
    df_kc_houses = get_df_houses_data()
    df_kc_houses.drop(columns=["id", "sqft_living15", "sqft_lot15"], inplace=True, errors="coerce")
    df_kc_houses.drop_duplicates(inplace=True)
    df_kc_houses["renovated"] = df_kc_houses["yr_renovated"].apply(lambda x: 1 if x > 0 else 0)
    df_kc_houses["log_price"] = np.log(df_kc_houses["price"])
    df_kc_houses[["waterfront", "zipcode", "view"]] = df_kc_houses[["waterfront", "zipcode", "view"]].astype(str)
    df_kc_houses.drop(columns=["date", "yr_renovated", "price", "yr_built"], inplace=True, errors="coerce")

    X = df_kc_houses.drop(columns=["log_price"])
    y = df_kc_houses["log_price"]

    cat_cols = X.select_dtypes(include="object").columns.tolist()
    
    X = df_kc_houses.drop(columns=["log_price"])
    y = df_kc_houses["log_price"]


    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(drop="first", sparse_output=False), cat_cols),
        ],remainder="passthrough")

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression()),
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    pipeline.fit(X_train, y_train)
    
    print("R2 Train:", pipeline.score(X_train, y_train))
    print("R2 Test: ", pipeline.score(X_test, y_test))
    
    save_schema(X_train, "artifacts/input_schema_predict_v0.1.0.json")
    
    with open("artifacts/modelo_lineal_v0.1.0.pkl", "wb") as f:
        pickle.dump(pipeline, f)
