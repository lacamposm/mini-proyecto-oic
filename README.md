# 🧠 OIC Model Service — Sistema de Predicción en Producción

Este repositorio contiene un sistema completo de predicción basado en regresión lineal, que expone una **API RESTful** con [FastAPI](https://fastapi.tiangolo.com/), una **interfaz web** en [Streamlit](https://streamlit.io/) y una **base de datos PostgreSQL**, todo completamente **dockerizado y preparado para producción**.

---

## Estructura del Proyecto

```plaintext
mini-proyecto-oic/
├── artifacts/
│   └── input_schema_predict_v0.1.0.json
│   └── kc_house_data.csv
│   └── modelo_lineal_v0.1.0.pkl
├── docs/
│   ├── source/
│   │   ├── config.py
│   │   ├── index.rst
│   │   ├── model.rst
│   │   ├── modules.rst
│   │   ├── oic_model_server.rst
│   │   ├── streamlit_app.rst
│   ├── make.bat
│   └── Makefile
├── model/
│   ├── __init__.py
│   ├── regression_model.py
│   └── run_training.py
│   └── utils.py
├── oic_model_server/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── predict.py
│   │       └── user.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   ├── raw_data.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── predict_service.py
│   │   ├── raw_data_service.py
│   │   └── user_service.py
│   ├── __init__.py
│   └── main.py
├── streamlit_app/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   └── history.py
│   │   └── prediction.py
│   │   └── user_managenebt.py
│   └── app.py
├── Dockerfile
├── docker-compose.yml
├── environment.yml
├── streamlit_app.py
└── README.md
```

---

## Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/lacamposm/mini-proyecto-oic.git
cd mini-proyecto-oic
```

## Paso 2: Uso del Dockerfile

El proyecto ofrece varias formas de trabajar con `Docker` según tus necesidades:

### 1. Construcción de la Imagen

Ejecuta el siguiente comando para construir la imagen desde el `Dockerfile`:

```sh
docker build -t oic-model-service .
```

Si la construcción fue exitosa, verás la imagen creada en tu lista de imágenes Docker:

```sh
docker images
```

### 2. Opciones para Ejecutar los Contenedores

#### Opción A: Shell Interactivo

Para acceder a un shell interactivo dentro del contenedor:

```sh
docker run -it --rm oic-model-service /bin/bash
```

Este comando te permite explorar el contenedor y verificar la instalación de dependencias:

```sh
conda list
```

#### Opción B: Desarrollo con Volúmenes Montados

Para desarrollar mientras los cambios se reflejan en tiempo real:

- Linux:

    ```sh
    docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") oic-model-service /bin/bash
    ```

- Windows:

    ```powershell
    docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf ${PWD})" -w "/$(Split-Path -Leaf ${PWD})" oic-model-service /bin/bash
    ```


Este comando:
- Monta el directorio actual como un volumen en el contenedor
- Establece el directorio de trabajo al nombre de la carpeta actual
- Abre un shell interactivo

#### Opción C: Servicio VS-codeserver.

Para ejecutar codeserver como IDE en el puerto 8000:

- Linux:

    ```sh
    docker run -it --rm -p 8080:8080 -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") oic-model-service
    ```

- Windows:

    ```powershell
    docker run -it --rm -p 8000:8000 -v "${PWD}:/$(Split-Path -Leaf ${PWD})" -w "/$(Split-Path -Leaf ${PWD})" oic-model-service
    ```

Este comando:
- Expone el puerto 8080 para VS-codeserver. 
- Monta el directorio actual como volumen
- Permite acceder a los servicios desde el navegador local

Una vez que el contenedor esté en ejecución, podrás acceder al IDE en:

- **VS Code-Server:** [http://localhost:8080/?folder=/mini-proyecto-oic](http://localhost:8080/?folder=/mini-proyecto-oic)


Para salir de cualquier contenedor interactivo, usa:

```sh
exit
```

## Paso 3: Construcción y Ejecución de Servicios con docker-compose

Después de haber construido y probado la imagen Docker, podemos proceder a levantar los servicios completos utilizando `docker-compose`.

---

### 1. Configuración de `docker-compose.yml`

Revisa el archivo `docker-compose.yml` ademas no olvides crear el archivo `.env` en la raiz del proyecto siguiendo el template en `.env.example`

### 2. Construcción y Levantamiento de Servicios

Existen varias formas de levantar los servicios con docker-compose:

#### Opción A: Levantar servicios con un nombre de proyecto personalizado

```sh
docker-compose -p oic-api-service up
```

Este comando:
- Asigna el nombre "oic-api-service" al proyecto
- Levanta todos los contenedores definidos en `docker-compose.yml`
- Muestra los logs en la terminal (modo interactivo)

#### Opción B: Construir y levantar servicios en un solo paso

```sh
docker-compose -p oic-api-service up --build
```

Este comando:
- Fuerza la reconstrucción de las imágenes
- Levanta los servicios después de la construcción
- Útil cuando hay cambios en el código que requieren una nueva construcción

#### Opción C: Ejecutar en segundo plano

```sh
docker-compose build
docker-compose up -d
```

Este proceso:
- Construirá la imagen si no existe
- Levantará los contenedores definidos en `docker-compose.yml` en modo detached (segundo plano)
- Iniciará la API con `FastAPI`, la interfaz gráfica con `Streamlit` y la base de datos `PostgreSQL`

***Nota:*** 
 Para verificar que los contenedores están corriendo, usa el siguiente comando:

  ```sh
  docker-compose ps
  ```

### 3. Verificación de Servicios Completos.

Una vez iniciados los servicios, verifica que estén accesibles:

- **FastAPI (API y Documentación):**  
  [http://localhost:8000/docs](http://localhost:8000/docs)

  Puedes probar la API enviando una solicitud con `curl`:

  ```sh
  curl -X 'POST' \
  'http://localhost:8000/predict/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "bathrooms": 2.25,
  "bedrooms": 3,
  "condition": 3,
  "floors": 2,
  "grade": 8,
  "lat": 47.6307,
  "long": -122.0412,
  "renovated": 0,
  "sqft_above": 1800,
  "sqft_basement": 0,
  "sqft_living": 1800,
  "sqft_lot": 7200,
  "user_name": "juan_perez",
  "view": "0",
  "waterfront": "0",
  "zipcode": "98052"
  }'
  ```
  La API responderá con:

    ```json
    {
      "prediction": 250000
    }
    ```

- **Streamlit (Interfaz Gráfica):**  
  [http://localhost:8501](http://localhost:8501)

   La interfaz de usuario te permitirá ingresar valores y recibir predicciones en tiempo real.

- **code-server (IDE en Navegador):** 

  [http://localhost:8080/?folder=/mini-proyecto-oic](http://localhost:8080/?folder=/mini-proyecto-oic)

  Te permite acceder a un IDE en el navegador para construir o editar tu proyecto en tiempo real.

- **PostgreSQL (Base de Datos):**  
  La base de datos corre en `localhost:5433`. Puedes conectarte usando un cliente como `pgAdmin` o `psql`.

### 4. Administración de Contenedores

Si necesitas ver los logs de los servicios en tiempo real, ejecuta:

```sh
docker-compose logs -f
```

Para detener los servicios:

```sh
docker-compose down
```

Para detener los servicios y eliminar volúmenes:

```sh
docker-compose down -v
```

---

## Servicios Independientes


### 1. Iniciar un servicio dev

```sh
docker-compose -p oic-dev up oic-model-postgis oic-model-api oic-codeserver
```

Este comando:

- Inicia un servicio para desarrollar en el proyecto.
- Mantiene el nombre de proyecto consistente con el resto del stack.
- Es útil cuando necesitas desarrollar sobre el proyecto completo (API-MODEL-UI).

Una vez que el contenedor esté en ejecución, podrás acceder al IDE en:

- **VS Code-Server:** [http://localhost:8080/?folder=/mini-proyecto-oic](http://localhost:8080/?folder=/mini-proyecto-oic)

### 2. Iniciar solo el servicio de PostgreSQL

```sh
docker-compose -p oic-postgis up oic-model-postgis
```

Este comando:
- Inicia únicamente el servicio de base de datos PostgreSQL
- Mantiene el nombre de proyecto consistente con el resto del stack
- Es útil cuando necesitas trabajar solo con la base de datos sin levantar otros servicios
- Permite realizar pruebas de conexión, modificaciones de esquema o consultas directas

Una vez inicializado el servicio de PostgreSQL, puedes conectarte a él usando:

```sh
docker exec -it oic-postgis psql -U postgres -d postgres
```


Para verificar que la base de datos está funcionando correctamente, puedes listar las tablas disponibles 
con:

```sql
\dt
```
    
Para consultar las predicciones almacenadas en la base de datos:

```sql
SELECT * FROM predictions;
```

Si necesitas realizar cambios en la estructura de la base de datos, puedes acceder a la terminal interactiva de `PostgreSQL` dentro del contenedor.





## Contribuciones

Si eres miembro del equipo y deseas contribuir, por favor sigue estas directrices:

1. Crea una rama para tu feature o corrección de errores desde la rama principal (`git checkout -b feature/nueva-funcionalidad`).
2. Realiza los cambios necesarios y haz commit de tus modificaciones (`git commit -m 'Añadir nueva funcionalidad'`).
3. Haz push a tu rama (`git push origin feature/nueva-funcionalidad`).
4. Abre un Pull Request (PR) en GitHub y describe los cambios realizados.
5. Asegúrate de que tu código cumpla con las normas de estilo.
6. Espera la revisión de tus compañeros de equipo y realiza los ajustes necesarios según sus comentarios.
