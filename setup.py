#!/usr/bin/env python

from __future__ import with_statement
import distutils.core
import sys
import shutil
import os
import ConfigParser

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

home_folder = os.getenv("HOME")
tmuxer_system_folder = home_folder + "/.tmuxer"
if not os.path.isdir(tmuxer_system_folder):
    os.mkdir(tmuxer_system_folder)

if not os.path.isdir(tmuxer_system_folder + '/samples'):
    os.mkdir(tmuxer_system_folder + '/samples')

if not os.path.isdir(tmuxer_system_folder + '/tmux_files'):
    os.mkdir(tmuxer_system_folder + '/tmux_files')

if os.path.exists(tmuxer_system_folder + '/samples/sample.yml'):
    os.remove(tmuxer_system_folder + '/samples/sample.yml')

shutil.copy('samples/sample.yml', tmuxer_system_folder + '/samples/')

if os.path.exists(tmuxer_system_folder + '/config'):
    os.remove(tmuxer_system_folder + '/config')

config = ConfigParser.RawConfigParser()
config.add_section('global')
config.set('global', 'editor', 'vim')

with open(tmuxer_system_folder + '/config') as configfile:
    config.write(configfile)

distutils.core.setup(name='Tmuxer',
      version='1.0',
      description='Python tmux layouts and panes manipulator',
      author='Marian Ignev',
      author_email='m@ignev.net',
      url='http://m.ignev.net/code/tmuxer',
      packages=['tmuxer'],
      package_dir={"tmuxer":"tmuxer"},
      install_requires = ['pyyaml'],
      scripts= ["bin/tmuxer"],
     )
