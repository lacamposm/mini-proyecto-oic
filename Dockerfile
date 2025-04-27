# Visita https://hub.docker.com/r/lacamposm/docker-helpers para más información sobre esta imagen base
FROM lacamposm/docker-helpers:python-conda-base-latest

# Crear carpeta del proyecto
WORKDIR /mini-proyecto-oic

# Instalar dependencias del sistema necesarias (p. ej. para psycopg2 o compilar extensiones)
RUN apt-get update && \
    apt-get install -y build-essential postgresql-client && \
    apt-get clean

# Copiar environment.yml y crear entorno conda
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean --all --yes && \
    rm /tmp/environment.yml

# Copiar código del backend (API), frontend (UI), y artifacts
COPY ./oic_model_server /mini-proyecto-oic/oic_model_server
COPY ./streamlit_app /mini-proyecto-oic/streamlit_app
COPY ./artifacts /mini-proyecto-oic/artifacts

# Activación automática del entorno conda
RUN echo 'eval "$(conda shell.bash hook)"' >> ~/.bashrc && \
    echo 'conda activate oic-model-server' >> ~/.bashrc

# Exponer puertos para API y Streamlit
EXPOSE 8000 8501