FROM python:3

# Install.
#RUN \
#  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
#  apt-get update && \
#  apt-get -y upgrade && \
#  apt-get install -y build-essential && \
#  apt-get install -y software-properties-common && \
#  apt-get install -y byobu curl git htop man unzip vim wget && \
#  apt-get install -y python3.6 && \
#  rm -rf /var/lib/apt/lists/*
COPY . /alias
WORKDIR /alias
RUN pip install gunicorn
RUN pip install -r requirements
EXPOSE 5000