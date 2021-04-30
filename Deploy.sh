#!/bin/bash

sudo docker stop violas-eod-service
sudo docker rm violas-eod-service
sudo docker image rm violas-eod-service
sudo docker image build --no-cache -t violas-eod-service .
sudo docker run --name=violas-eod-service --network=host -d violas-eod-service
