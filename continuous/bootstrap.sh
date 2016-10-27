#!/usr/bin/env bash

sudo apt-get -y update
sudo apt-get -y install redis-server
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install python3-pip
python3 -m pip install --upgrade pip
cd /utubeu
python3 -m pip install -r requirements.txt
echo "alias python=python3" >> ~/.bashrc

