#!/usr/bin/env bash

sudo apt-get -y update
sudo apt-get -y install redis-server
sudo apt-get -y install postgresql-9.5 postgresql-contrib-9.5 postgresql-server-dev-9.5
sudo apt-get -y install python3-pip
python3 -m pip install --upgrade pip
cd /vagrant
python3 -m pip install -r requirements.txt
echo "alias python='python3'" >> ~/.bashrc

