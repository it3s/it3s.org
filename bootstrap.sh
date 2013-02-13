#! /usr/bin/env sh

sudo apt-get install nodejs npm python-dev -y

# install local python packages
pip install -r requirements.txt

sudo npm install -g coffee-script@1.2
sudo npm install -g less@1.3.1

# install local nodejs packages from package.json
npm install
