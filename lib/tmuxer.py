from __future__ import with_statement
from datetime import datetime
import yaml
import os

def main():
    with open('/Users/mignev/Documents/tmuxer/samples/appsc.yml', 'r') as yaml_stream:
        parser(yaml_stream)

def parser(yaml_stream):
    yml = yaml.load(yaml_stream)
    tmux_file_lines = list()

    tmux_file_lines.append('#!/bin/bash\n') 
    tmux_file_lines.append('cd ' + yml['project_root'] + '\n')
    tmux_file_lines.append('tmux start-server\n')
    tmux_file_lines.append("if ! $(tmux has-session -t '{0}'); then\n".format(yml['project_name']))

    print('#!/bin/bash')
    print('cd ' + yml['project_root'])
    print(yml['project_name'])
    print(yml['project_root'])

    for tab in yml['tabs']:
        print(tab)
    #os.system('vim appsc.sh')

    print('after os {0}:{1}:{2}'.format(datetime.now().hour, datetime.now().minute, datetime.now().second))

    with open('/tmp/somenew_file', 'w') as tmux_file:
        tmux_file.writelines(tmux_file_lines)

if __name__ == '__main__':
    main()
