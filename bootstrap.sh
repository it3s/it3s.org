#! /usr/bin/env sh

sudo apt-get install nodejs npm python-dev -y

# install local python packages
pip install -r settings/requirements.txt

sudo npm install -g coffee-script@1.2
sudo npm install -g less@1.3.1
