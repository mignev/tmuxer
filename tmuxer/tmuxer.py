from __future__ import with_statement
from re import search
import yaml
import os
import sys
import shutil
import ConfigParser

class Tmuxer:
    def __init__(self):
        self.tmuxer_dir = os.getenv('HOME') + '/.tmuxer'
        self.sample_conf = self.tmuxer_dir + '/samples/sample.yml'
        self.compiled_files = self.tmuxer_dir + '/tmux_files/'
        self.shell = os.getenv("SHELL")

        self.struct = dict()

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
            self._project_name = yml['project_name']
            tmux_file_lines = list()
            
            tmux_file_lines.append('#!'+self.shell+'\n')
            tmux_file_lines.append('cd ' + yml['project_root'] + '\n')
            tmux_file_lines.append('tmux start-server\n\n')
            tmux_file_lines.append("if ! $(tmux has-session -t '{0}'); then\n\n".format(yml['project_name']))

            tmux_file_lines.append("\n# set up tabs and panes\n\n")

            tab_counter = 0
            for tab in yml['tabs']:
                tmux_file_lines.append('# tab "{0}"\n'.format(tab['name']))
                if tab_counter == 0:
                    tmux_file_lines.append("tmux new-session -d -s '{0}' -n '{1}'\n".format(yml['project_name'], tab['name']))
                else:
                    tmux_file_lines.append("tmux new-window -t '{0}':{1} -n '{2}'\n".format(yml['project_name'], tab_counter, tab['name']))

                if tab.has_key('layout'):
                    layout = tab['layout']
                    tmux_file_lines.append("tmux select-layout -t '{0}':{1} '{2}'\n\n".format(yml['project_name'], tab_counter,  layout))

                
                start_pane_id = start_parent_id = 0
                #print(tab)
                #sys.exit()	

                if tab.has_key('panes'):
                    tmux_file_lines += self._process_panes( tab['panes'], tab_counter, start_pane_id, start_parent_id )

                tab_counter += 1

            tmux_file_lines.append("\ttmux -u select-window -t '{0}':0\n".format(yml['project_name']))

            tmux_file_lines.append("\nfi\n")
            
            tmux_file_lines.append("\nif [ -z $TMUX ]; then\n")
            tmux_file_lines.append("\ttmux -u attach-session -t '{0}'\n".format(yml['project_name']))
            
            tmux_file_lines.append("else\n")
            tmux_file_lines.append("\ttmux -u switch-client -t '{0}'\n".format(yml['project_name']))
            tmux_file_lines.append("fi\n")

            with open(self.compiled_files + self.current_project + '.tmux', 'w') as tmux_file:
                tmux_file.writelines(tmux_file_lines)
    
    def _process_panes(self, panes, tab_id, pane_id, parent_pane_id):
        lines = list()
        for pane in panes:
            lines.append("tmux select-window -t '{0}':{1}\n".format(self._project_name, tab_id))

            if pane_id != 0:
                if pane.has_key('split'):
                    lines.append("tmux splitw -{0}\n".format(pane['split'][0]))
                else:
                    lines.append("tmux splitw\n".format(parent_pane_id))
            
            lines.append("tmux select-pane -t {0}\n".format(pane_id))

            if pane.has_key('resize'):
                resize_kw = {'left': '-L', 'right': '-R', 'up': '-U', 'down': '-D'}
                for resize in pane['resize']:
                    lines.append("tmux resize-pane {0} {1}\n".format(resize_kw[ str(resize.keys()[0]) ], resize.values()[0] ))

            if isinstance(pane['cmd'], list):
                for cmd in pane['cmd']:
                    lines.append("tmux send-keys -t '{0}':{1} '{2}' C-m\n".format(self._project_name, tab_id, cmd))
            else:
                lines.append("tmux send-keys -t '{0}':{1} '{2}' C-m\n".format(self._project_name, tab_id, pane['cmd']))

            lines.append('\n')
            pane_id += 1

        return lines
    
    def delete(self, project_name):
        project_config_file = self.tmuxer_dir + '/' + project_name + '.yml'
        project_tmux_file = self.compiled_files + '/' + project_name + '.tmux'
        if os.path.exists(project_config_file):
            os.remove(project_config_file)
            os.remove(project_tmux_file)

    def run_project(self, project_name):
        project_tmux_file = self.compiled_files + '/' + project_name + '.tmux'
        if os.path.exists(project_tmux_file):
            os.system( self.shell +' '+ project_tmux_file )
        else:
            print('\nProject ' + project_name + ' does not exist!\n')
            print('To create project with this name type this:')
            print('  tmuxer open ' + project_name)

    def projects_list(self):
        for filename in os.listdir(self.tmuxer_dir):
            if search(r'.yml', filename):
                project_name = filename[:-4]
                print(project_name)

    
if __name__ == '__main__':
    #for development purposes
    tmuxer = Tmuxer()
    tmuxer.open('tmuxer')
