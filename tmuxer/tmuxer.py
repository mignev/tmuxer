from __future__ import with_statement
from datetime import datetime
import yaml
import os
import shutil
import ConfigParser

class Tmuxer:
    def __init__(self):
        self.tmuxer_dir = os.getenv('HOME') + '/.tmuxer'
        self.sample_conf = self.tmuxer_dir + '/samples/sample.yml'
        self.compiled_files = self.tmuxer_dir + '/tmux_files/'

        _config_path = self.tmuxer_dir + '/config'
        config = ConfigParser.RawConfigParser()
        config.read(_config_path)

        self.editor = config.get('global', 'editor')

    def open(self, project_name):
        self.current_project = project_name
        target_project_file = self.tmuxer_dir + '/' + self.current_project + '.yml'

        if os.path.exists(target_project_file):
            os.system(self.editor + ' ' + target_project_file)
        else:
            shutil.copy(self.sample_conf, target_project_file)
            os.system(self.editor + ' ' + target_project_file)

        return self._process_yml(target_project_file)

    def _process_yml(self, _yml_file):
        with open(_yml_file, 'r') as yml_stream:
            yml = yaml.load(yml_stream)
            print(yml)
            tmux_file_lines = list()
            
            tmux_file_lines.append('#!/bin/bash\n') 
            tmux_file_lines.append('cd ' + yml['project_root'] + '\n')
            tmux_file_lines.append('tmux start-server\n\n')
            tmux_file_lines.append("if ! $(tmux has-session -t '{0}'); then\n\n".format(yml['project_name']))

            tmux_file_lines.append("tmux select-window -t '{0}':0\n".format(yml['project_name']))
            
            tmux_file_lines.append("\n# set up tabs and panes\n\n")

            tab_counter = 0
            for tab in yml['tabs']:
                tmux_file_lines.append('# tab "{0}"\n'.format(tab['name']))
                if tab_counter == 0:
                    tmux_file_lines.append("tmux new-session -d -s '{0}' -n '{1}'\n".format(yml['project_name'], tab['name']))
                else:
                    tmux_file_lines.append("tmux new-window -t '{0}':{1} -n '{2}'\n".format(yml['project_name'], tab_counter, tab['name']))
                self._process_panes(tab['panes'], tab_counter)
                tab_counter += 1

            tmux_file_lines.append("\nfi\n")
            
            tmux_file_lines.append("\nif [ -z $TMUX ]; then\n")
            tmux_file_lines.append("\ttmux -u attach-session -t '{0}'\n".format(yml['project_name']))
            
            tmux_file_lines.append("else\n")
            tmux_file_lines.append("\ttmux -u switch-client -t '{0}'\n".format(yml['project_name']))
            tmux_file_lines.append("fi\n")

            with open(self.compiled_files + self.current_project + '.tmux', 'w') as tmux_file:
                tmux_file.writelines(tmux_file_lines)
    
    def _process_panes(self, panes, tab_id):
        pass

if __name__ == '__main__':
    tmuxer = Tmuxer()
    tmuxer.open('appsc')
