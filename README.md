Tmuxer is a simple python app who helps you to set up windows, panes and layouts for tmux using YAML configs.

The idea for Tmuxer is inspired from these two projects:

* Tmuxinator - http://github.com/aziz/tmuxinator
* Teamocil - http://github.com/remiprev/teamocil

Thank you guys :)

#Installation

Installation with `make`

    make install

Installation without `make`

    python setup.py build
    sudo python setup.py install 

#Example

![Example](http://oi55.tinypic.com/f2u55f.jpg)


#Usage

Creating new project

    tmuxer open project_name

Editing existing project

    tmuxer open project_name

Deleting a project

    tmuxer rm/del project_name

Running a project
    
    tmuxer run project_name

Prints a list with all existing projects

    tmuxer ls

Prints a current `tmuxer` version

    tmuxer version

#Copyright

Copyright (c) 2011 Marian Ignev. See LICENSE for further details.
