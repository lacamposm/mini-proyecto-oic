# https://hub.docker.com/r/lacamposm/docker-helpers for more information
FROM lacamposm/docker-helpers:python-conda-base-latest

# Create project directory
WORKDIR /mini-proyecto-oic

# Install required system dependencies (e.g., for psycopg2 or to compile extensions)
RUN apt-get update && \
    apt-get install -y build-essential postgresql-client && \
    apt-get clean
    apt-get install -y build-essential postgresql-client && \
    apt-get clean

# Copy environment.yml and create conda environment
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean --all --yes && \
    rm /tmp/environment.yml

# Copy backend (API), frontend (UI), and artifacts
COPY ./oic_model_server /mini-proyecto-oic/oic_model_server
COPY ./streamlit_app /mini-proyecto-oic/streamlit_app
COPY ./artifacts /mini-proyecto-oic/artifacts

# Enable automatic activation of the conda environment
RUN echo 'eval "$(conda shell.bash hook)"' >> ~/.bashrc && \
    echo 'conda activate oic-model-server' >> ~/.bashrc

# Expose ports for API and Streamlit
EXPOSE 8000 8501