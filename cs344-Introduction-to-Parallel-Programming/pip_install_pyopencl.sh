#!/usr/bin/env sh
sudo apt-get install python-pip python-dev
sudo pip install virtualenv virtualenvwrapper

echo 'export PROJECT_HOME="$HOME/src"' >> $HOME/.bashrc
echo 'export WORKON_HOME="$HOME/.virtualenvs"' >> $HOME/.bashrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> $HOME/.bashrc

sudo apt-get install -y gfortran g++
# sudo apt-get remove -y --purge python-setuptools

# start a new virtalenv project
mkproject parallel
pip install --upgrade distribute
pip install mako numpy pyopencl

