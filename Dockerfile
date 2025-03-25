# Visita: https://hub.docker.com/r/lacamposm/docker-helpers/tags
# Para ver mas imagenes base disponibles.
FROM lacamposm/docker-helpers:conda-vscode

WORKDIR /mini-proyecto-oic

# Herramientas para paquetes adicionales (PostgreSQL)
RUN apt-get update && \
    apt-get install -y build-essential postgresql-client

COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && rm /tmp/environment.yml

# Activación automática del entorno conda
RUN echo 'eval "$(conda shell.bash hook)"' >> ~/.bashrc && \
    echo 'conda activate oic-model-server' >> ~/.bashrc

# Puerto para streamlit, uvicorn y code-server
EXPOSE 8501 8000 8080