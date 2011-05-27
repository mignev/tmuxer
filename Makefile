help:
	@echo "   install      to install Tmuxer"
	@echo "   uninstall    to uninstall Tmuxer"
	@echo "   clean        to clean useless files"

install:
	@echo "Installing"
	@sudo python setup.py install --record installed_files.txt
uninstall:
	@cat installed_files.txt | xargs rm -rf
	@sudo rm installed_files.txt	
	@sudo rm -rf ~/.tmuxer

clean:
	@sudo rm -rf Tmuxer.egg*
	@sudo rm -rf dist
	@sudo rm -rf build