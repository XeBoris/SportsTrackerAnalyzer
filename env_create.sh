#!/bin/bash

ENVNAME=.env

#Create
python -m venv $PWD/${ENVNAME}

#update with requrirements:
echo $PWD/${ENVNAME}/bin/activate
source $PWD/${ENVNAME}/bin/activate

pip install -r requirements.txt

deactivate