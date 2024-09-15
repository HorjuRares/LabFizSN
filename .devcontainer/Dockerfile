FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN pip3 install neuron
RUN pip3 install matplotlib
RUN pip3 install plotly
RUN pip3 install efel
RUN pip3 install numpy
RUN pip3 install torch torchvision torchaudio
RUN pip3 install spikingjelly
RUN pip install tensorboard

RUN sudo apt-get update
RUN sudo apt-get upgrade -y
RUN sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 2