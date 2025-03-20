# Mini Proyecto OIC

Este repositorio contiene un modelo analítico basado en regresión lineal, integrado con FastAPI, PostgreSQL y una 
interfaz gráfica desarrollada en Streamlit, todo encapsulado y dockerizado para facilitar el despliegue.

---

## Estructura del Proyecto


```plaintext
mini-proyecto-oic/
├── data/
│   └── house_prices.csv
├── models/
│   └── modelo_regresion.pkl
├── src/
│   └── oic_model_houses/
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes/
│       │       └── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── prediction.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── prediction_service.py
│       ├── __init__.py
│       ├── main.py
│       ├── regression_model.py
│       └── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── environment.yml
└── README.md
```

---

## Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/lacamposm/desarrollo-analitico-oic.git
cd mini-proyecto-oic
```

## Paso 2: Uso del Dockerfile

Vamos a construir y probar la imagen Docker de forma independiente.

### 1. Construcción de la Imagen

Ejecuta el siguiente comando para construir la imagen desde el `Dockerfile`:

```sh
docker build -t mini-proyecto-oic .
```

Si la construcción fue exitosa, verás una salida similar a esta:
```sh
REPOSITORY TAG IMAGE ID CREATED SIZE mini-proyecto-oic latest abc123456789 X minutes ago 1.2GB
```

---

### 2. Creación de un Contenedor

Para probar la imagen antes de usar `docker-compose`, ejecuta un contenedor de manera manual:

```sh
docker run --rm -it mini-proyecto-oic bash
```

Este comando iniciará un shell interactivo dentro del contenedor. Dentro de este, puedes verificar que el entorno de 
Conda esté activo y que las dependencias estén correctamente instaladas ejecutando:

```sh
bash
conda list
```

Si todo está correcto, deberías ver la lista de paquetes instalados.

Para salir del contenedor, usa:

```sh
exit
```

## Paso 3: Construcción y Ejecución de Servicios con Docker Compose

Después de haber construido y probado la imagen Docker, podemos proceder a levantar los servicios completos utilizando `docker-compose`.

---

### 1. Configuración de `docker-compose.yml`

Asegúrate de que el archivo `docker-compose.yml` esté correctamente configurado.

### 2. Construcción y Levantamiento de Servicios

Ejecuta los siguientes comandos para construir y ejecutar los servicios en segundo plano:

```sh
docker-compose build
docker-compose up -d
```

Este proceso:

- **Construirá la imagen** si no existe.
- **Levantará los contenedores** definidos en `docker-compose.yml`.
- **Iniciará la API con FastAPI**, la interfaz gráfica con Streamlit y la base de datos PostgreSQL.

Para verificar que los contenedores están corriendo, usa el siguiente comando:

```sh
docker-compose ps
```

Si los servicios están funcionando correctamente, deberías ver una salida similar a esta:

```nginx
   Name                      Command               State           Ports
----------------------------------------------------------------------------------
mini-proyecto-oic-app-1      "uvicorn src.api_..." Up      0.0.0.0:8000->8000/tcp
mini-proyecto-oic-db-1       "docker-entrypoin..." Up      0.0.0.0:5432->5432/tcp
```

### 3. Verificación de Servicios

Una vez iniciados los servicios, verifica que estén accesibles:

- **FastAPI (API y Documentación):**  
  [http://localhost:8000/docs](http://localhost:8000/docs)

  Puedes probar la API enviando una solicitud con `curl`:

  ```sh
  curl -X 'POST' 'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
    "feature1": 120.5,
    "feature2": 45.3,
    "feature3": "example_value"
  }'
  ```
  La API responderá con:

    ```json
    {
      "prediction": 250000.0
    }
    ```

- **Streamlit (Interfaz Gráfica):**  
  [http://localhost:8501](http://localhost:8501)

   La interfaz de usuario te permitirá ingresar valores y recibir predicciones en tiempo real.

- **PostgreSQL (Base de Datos):**  
  La base de datos corre en `localhost:5432`. Puedes conectarte usando un cliente como `pgAdmin` o `psql`:

  ```sh
  psql -h localhost -U user -d dbname
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
    
    Si necesitas realizar cambios en la estructura de la base de datos, puedes acceder a la terminal interactiva de 
    `PostgreSQL` dentro del contenedor:
    
    ```shell
    docker exec -it mini-proyecto-oic-db-1 psql -U user -d dbname
    ```

### 4. Administración de Contenedores

Si necesitas ver los logs de los servicios en tiempo real, ejecuta:

```sh
docker compose logs -f
```

## Contribuciones

Este es un repositorio privado. Si eres miembro del equipo y deseas contribuir, por favor sigue estas directrices:

1. Crea una rama para tu feature o corrección de errores desde la rama principal (`git checkout -b feature/nueva-funcionalidad`).
2. Realiza los cambios necesarios y haz commit de tus modificaciones (`git commit -m 'Añadir nueva funcionalidad'`).
3. Haz push a tu rama (`git push origin feature/nueva-funcionalidad`).
4. Abre un Pull Request (PR) en GitHub y describe los cambios realizados.
5. Asegúrate de que tu código cumpla con las normas de estilo.
6. Espera la revisión de tus compañeros de equipo y realiza los ajustes necesarios según sus comentarios.

Gracias por tu contribución al proyecto.



