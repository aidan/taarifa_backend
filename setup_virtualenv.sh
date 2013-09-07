#!/bin/bash

# Setup script for installing into a virtualenv to avoid messing with
# system packages

if [ ! -e /usr/bin/virtualenv ] ; then
    echo -e "virtualenv NOT found, run sudo easy_install virtualenv"
    exit 1
fi

export VIRTUALENV_PATH=${PWD}/virtualenv
virtualenv --no-site-packages $VIRTUALENV_PATH
source $VIRTUALENV_PATH/bin/activate

if [ ! -e $VIRTUALENV_PATH/bin/nosetests ] ; then
        easy_install nose
fi

pip install -r requirements.txt

echo "Run \"source $VIRTUALENV_PATH/bin/activate\" to activate this virtualenv."


