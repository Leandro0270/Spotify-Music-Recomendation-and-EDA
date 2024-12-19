FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    libtiff5 libjpeg-dev zlib1g-dev libfreetype6 liblcms2-dev libwebp-dev tcl8.6 tk8.6 python3-tk \
    libopenblas-dev libomp-dev wget curl && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda init

ENV PATH="/opt/conda/bin:$PATH"

RUN conda create -n rapids-22.12 -c rapidsai -c nvidia -c conda-forge \
    cuml=22.12 python=3.9 cudatoolkit=11.8 seaborn matplotlib plotly scikit-learn pandas numpy -y && \
    conda clean -a -y

SHELL ["conda", "run", "-n", "rapids-22.12", "/bin/bash", "-c"]

WORKDIR /workspace
