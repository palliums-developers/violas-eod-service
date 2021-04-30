FROM ubuntu

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install git python3 python3-pip

RUN git clone -b v0.30 https://Xing-Huang:13583744689edc@github.com/palliums-developers/violas-client.git violas-client
RUN pip3 install -r /violas-client/requirements.txt

COPY . /violas-eod-service
RUN pip3 install -r /violas-eod-service/requirements.txt

WORKDIR /violas-eod-service
RUN cp -rf ../violas-client/violas_client .

CMD ["python3", "Main.py"]