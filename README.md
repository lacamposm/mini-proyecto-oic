# 🧠 OIC Model Service — Sistema de Predicción de Precios de Inmuebles

Este repositorio contiene un sistema completo de predicción basado en regresión lineal, que expone una **API RESTful** con [FastAPI](https://fastapi.tiangolo.com/), una **interfaz web** en [Streamlit](https://streamlit.io/) y una **base de datos PostgreSQL/PostGIS**, todo completamente **dockerizado y preparado para desarrollo**.

---

## Estructura del Proyecto

```plaintext
mini-proyecto-oic/
├── .devcontainer/
│   ├── Dockerfile.dev
│   ├── Dockerfile.ui
│   ├── docker-compose-dev.yml
│   ├── environment.ui.yml
│   └── devcontainer.json
├── artifacts/
│   ├── input_schema_predict_v0.1.0.json
│   ├── kc_house_data.csv
│   └── modelo_lineal_v0.1.0.pkl
├── docs/
│   ├── source/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── model.rst
│   │   ├── modules.rst
│   │   ├── oic_model_server.rst
│   │   ├── streamlit_app.rst
│   │   └── _static/
│   │       ├── logo_OIC_blue.png
│   │       └── logo_python.jpg
│   ├── make.bat
│   └── Makefile
├── model/
│   ├── regression_model.py
│   ├── run_training.py
│   └── utils.py
├── oic_model_server/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── predict.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── predict.py
│   │   ├── raw_data.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── predict_service.py
│   │   ├── raw_data_service.py
│   │   ├── user_service.py
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── streamlit_app/
│   ├── components/
│   │   ├── history.py
│   │   ├── prediction.py
│   │   ├── user_management.py
│   │   └── __init__.py
│   ├── app.py
│   └── __init__.py
├── Dockerfile
├── docker-compose.yml
├── environment.yml
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
docker images | grep oic-model-service
```

### 2. Opciones para Ejecutar los Contenedores

#### Opción A: Shell Interactivo

Para acceder a un shell interactivo dentro del contenedor:

```sh
docker run -it --rm oic-model-service /bin/bash
```

Este comando te permite explorar el contenedor y verificar los entornos conda instalados:

```sh
conda env list
```

#### Opción B: Desarrollo con Volúmenes Montados

Para desarrollar mientras los cambios se reflejan en tiempo real:

- Linux/macOS:

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

Para salir de cualquier contenedor interactivo, usa:

```sh
exit
```

**Nota:** Para un entorno de desarrollo completo, recomendamos usar VS Code con Dev Containers como se describe en la sección "Desarrollo con Visual Studio Code y Dev Containers" más adelante en este documento.

## Paso 3: Construcción y Ejecución de Servicios con docker-compose

Después de haber construido y probado la imagen Docker, podemos proceder a levantar los servicios completos utilizando `docker-compose`.

---

### 1. Configuración de Variables de Entorno

Antes de iniciar los servicios, crea un archivo `.env` en la raíz del proyecto siguiendo el template en `.env.example`:

```sh
# Copiar el archivo de ejemplo y configurar según necesidad
cp .env.example .env
```

Edita el archivo `.env` para establecer las variables de entorno necesarias, como la URL de la base de datos:

```
DATABASE_URL=postgresql://postgres:postgres@oic-model-postgis:5432/postgres
```

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

### 3. Verificación de Servicios

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
  
  La API responderá con una predicción similar a:

  ```json
  {
    "prediction": 250000
  }
  ```

- **Streamlit (Interfaz Gráfica):**  
  [http://localhost:8501](http://localhost:8501)

  La interfaz de usuario te permitirá ingresar valores y recibir predicciones en tiempo real.

- **Base de Datos PostgreSQL/PostGIS:**
  - Puerto: 5433 (mapeado desde 5432 del contenedor)
  - Usuario: postgres
  - Contraseña: postgres
  - Base de datos: postgres

### 4. Administración de Contenedores

Si necesitas ver los logs de los servicios en tiempo real, ejecuta:

```sh
docker-compose logs -f
```

Para detener los servicios:

```sh
docker-compose down
```

Para detener los servicios y eliminar volúmenes (¡cuidado! esto eliminará todos los datos almacenados):

```sh
docker-compose down -v
```

---

## Desarrollo con Visual Studio Code y Dev Containers

Este proyecto incluye configuración para desarrollo usando VS Code Dev Containers, lo que te permite trabajar dentro de un entorno Docker completamente configurado.

### 1. Requisitos previos

- [Visual Studio Code](https://code.visualstudio.com/)
- Extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) instalada
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) o Docker Engine (Linux)

### 2. Abrir en Dev Container

1. Abre VS Code
2. Presiona `F1` para abrir la paleta de comandos
3. Escribe y selecciona `Dev Containers: Open Folder in Container...`
4. Selecciona la carpeta de este proyecto

VS Code construirá y configurará automáticamente el contenedor según las especificaciones en `.devcontainer/devcontainer.json`, y luego abrirá la ventana conectada al contenedor.

El proyecto ofrece dos opciones para trabajar con Dev Containers:

#### Entorno de Desarrollo Optimizado (Recomendado)

El entorno de desarrollo utiliza Dockerfiles y docker-compose dedicados ubicados en el directorio `.devcontainer/`:

- `Dockerfile.dev`: Configurado específicamente para el desarrollo de la API
- `Dockerfile.ui`: Configurado específicamente para el desarrollo de la interfaz de usuario Streamlit
- `docker-compose-dev.yml`: Configuración separada de Docker Compose para desarrollo
- `environment.ui.yml`: Archivos de entorno específicos para la UI 
- Usuario no-root (`dev-user`) para mayor seguridad
- Volúmenes configurados para sincronizar todos los cambios entre host y contenedor
- Depuración integrada para FastAPI y Streamlit

Esta opción está configurada por defecto en el archivo `devcontainer.json`.

**¡IMPORTANTE!** Al abrir el proyecto en un Dev Container, te conectarás al servicio `oic-model-api`. El contenedor ya incluirá todas las herramientas necesarias para el desarrollo.

### 3. Beneficios del Dev Container

- Entorno de desarrollo consistente en cualquier máquina
- Todas las dependencias preinstaladas (Python, Conda, PostgreSQL client, etc.)
- Acceso directo a la base de datos y servicios definidos en `docker-compose.yml`
- Extensiones de VS Code preconfiguradas (Python, Pylance, Git, Debugpy, etc.)
- Formateo automático con Black configurado
- Linting con Pylint habilitado
- Sincronización bidireccional de archivos entre el host y el contenedor
- Configuración separada para servicios de API y UI

### 4. Puertos Disponibles

Los siguientes puertos están configurados para reenvío automático:
- 5432: PostgreSQL dentro del contenedor
- 5433: PostgreSQL mapeado al host
- 8000: API FastAPI
- 8501: Interfaz Streamlit
- 5678: Puerto para depuración remota.

---

## Servicios Independientes

### Iniciar solo el servicio de PostgreSQL/PostGIS

Cuando no necesitas el stack completo y solo quieres trabajar con la base de datos:

```sh
docker-compose -p oic-postgis up oic-model-postgis
```

Este comando:
- Inicia únicamente el servicio de base de datos PostgreSQL con extensión PostGIS
- Mantiene el nombre de proyecto consistente con el resto del stack
- Es útil cuando necesitas trabajar solo con la base de datos sin levantar otros servicios
- Permite realizar pruebas de conexión, modificaciones de esquema o consultas directas

Una vez inicializado el servicio de PostgreSQL, puedes conectarte a él usando:

```sh
docker exec -it oic-model-postgis psql -U postgres -d postgres
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

---

## Contribuciones

Al ser un repositorio público, agradecemos las contribuciones de la comunidad. Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio a tu cuenta de GitHub.
2. Crea una nueva rama para tu contribución (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y mejoras en la rama.
4. Asegúrate de que tu código cumpla con las normas de estilo del proyecto (usa Black para formateo).
5. Confirma tus cambios (`git commit -m 'Añadir nueva funcionalidad'`).
6. Empuja los cambios a tu fork (`git push origin feature/nueva-funcionalidad`).
7. Abre un Pull Request (PR) desde tu fork al repositorio original.
8. En la descripción del PR, explica claramente los cambios realizados y su propósito.
9. Espera la revisión y colabora con los mantenedores para abordar cualquier comentario o sugerencia.

Todas las contribuciones, grandes o pequeñas, son bienvenidas - desde correcciones de errores y mejoras en la documentación hasta nuevas funcionalidades.

## Licencia

Este proyecto se distribuye bajo los términos de la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

**Última actualización:** 27 de abril de 2025
