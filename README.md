Tmuxer is a simple python app who helps you to set up windows, panes and layouts for tmux using YAML configs.

The idea for Tmuxer is inspired from these two projects:

* Tmuxinator - http://github.com/aziz/tmuxinator
* Teamocil - http://github.com/remiprev/teamocil

Thank you guys :)

#Example

![Example](http://oi55.tinypic.com/f2u55f.jpg)

#Requirements

* Tmux (of course) - tested with Tmux 1.4
* Python 2.5+
* PyYAML (latest version recommended) - tested with PyYAML 3.10

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
