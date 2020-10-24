#!/bin/bash
#source $PWD/env_start.sh
#jupyter-notebook --config $PWD/Notebooks/config/jupyter_notebook_config.py

#Start a notebook and leave it running on TMUX
tmux new -d -s spTrAn 'source $PWD/env_start.sh; jupyter-notebook --config $PWD/Notebooks/config/jupyter_notebook_config.py' \;
