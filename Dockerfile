FROM lacamposm/docker-helpers:python-conda-notebooks-code-server

WORKDIR /mini-proyecto-oic

# Herramientas para paquetes adicionales (PostgreSQL)
RUN apt-get update && \
    apt-get install -y build-essential postgresql-client

COPY environment.yml environment.yml

RUN conda env create -f environment.yml

# Activación automática del entorno conda
RUN echo 'eval "$(conda shell.bash hook)"' >> ~/.bashrc && \
    echo 'conda activate oic-model-server' >> ~/.bashrc

# Puerto para streamlit, uvicorn, notebooks y code-server
EXPOSE 8501 8000 8888 8080