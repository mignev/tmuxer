Tmuxer is a simple python app who helps you to set up windows, panes and layouts for tmux using YAML configs.

#Installation

Installation with `make`

    make install

Installation without `make`

    python setup.py build
    sudo python setup.py install 

#Usage

Creating new project

    tmuxer open project_name

Editing existing project

    tmuxer open project_name

Deleting project

    tmuxer del project_name

Prints a list with all existing projects

    tmuxer ls

Prints a current `tmuxer` version

    tmuxer version
