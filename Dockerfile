FROM debian:bookworm-slim as carsten
RUN apt update && \
    apt install -y \
        libc6-dev \
        curl \
        m4 \
        libgmp-dev \
        libmpfr-dev \
        build-essential  \
        git \
        python3-dev \
        python3-venv \
        python3-pip && \
    python3 -m venv .venv && \
    .venv/bin/pip3 install Cython numpy wheel && \
    curl https://www.flintlib.org/flint-2.9.0.tar.gz --output flint-2.9.0.tar.gz && \
    tar -xf flint-2.9.0.tar.gz && \
    rm flint-2.9.0.tar.gz && \
    cd flint-2.9.0 && \
    ./configure && \
    make && \
    make install && \
    cd / && \
    rm -rf flint-2.9.0 && \
    git clone https://github.com/fredrik-johansson/arb.git && \
    cd arb && \
    ./configure && \
    make && \
    make install && \
    cd / && \
    rm -rf arb
COPY ./notebook.py .
COPY ./data.py .
COPY ./requirements.txt .
RUN .venv/bin/pip3 install -Ur requirements.txt
RUN apt install -y vim
