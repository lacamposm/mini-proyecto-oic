# 🧠 OIC Model Service — Sistema de Predicción en Producción

Este repositorio contiene un sistema completo de predicción basado en regresión lineal, que expone una **API RESTful** con [FastAPI](https://fastapi.tiangolo.com/), una **interfaz web** en [Streamlit](https://streamlit.io/) y una **base de datos PostgreSQL**, todo completamente **dockerizado y preparado para producción**.

---

## 🚀 Despliegue en Producción

### 1. Requisitos previos

- Docker ≥ 24
- Docker Compose ≥ v2
- Archivo `.env` correctamente configurado (puedes usar `.env.example` como base)

---

### 2. Construcción y levantamiento del servicio

```bash
docker-compose -f docker-compose.prod.yml up --build
```

---

## 🌐 Servicios disponibles

| Servicio      | URL local                         | Descripción                                 |
|---------------|-----------------------------------|---------------------------------------------|
| API           | http://localhost:8000/docs        | Documentación interactiva (Swagger UI)      |
| Streamlit     | http://localhost:8501             | Interfaz web para predicción                |
| Base de datos | `localhost:5433`                  | PostgreSQL (usuario: `postgres`)            |

---

## 📁 Estructura del Proyecto

```plaintext
mini-proyecto-oic/
├── oic_model_server/        # Lógica de negocio y API
├── streamlit_app/           # Interfaz web
├── artifacts/               # Modelo entrenado, esquema, dataset original
├── environment.prod.yml     # Entorno Conda congelado
├── Dockerfile.prod          # Dockerfile listo para producción
├── docker-compose.prod.yml  # Configuración de servicios en producción
├── .env.example             # Ejemplo de configuración
└── README.md
```