zip:
	$(abspath $(lastword $(MAKEFILE_LIST)))
	pip3 install pytest_terraform-0.6.1-py3-none-any.whl