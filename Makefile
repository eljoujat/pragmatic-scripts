.PHONY: install list chmod help

help:
	@echo "Targets: install, list, chmod"

install:
	python3 -m pip install -r requirements.txt

list:
	@find scripts -name '*.py' | sort

chmod:
	@find scripts -name '*.py' -exec chmod +x {} \;
