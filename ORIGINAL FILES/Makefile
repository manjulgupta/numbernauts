python_executable=python3
environment_name=.venv
py=$(environment_name)/bin/python3
SYMBOL?=BPCL
num_years?=5

.PHONY: all
all: $(environment_name)/pyvenv.cfg
	$(py) -m flask --debug run 

$(environment_name)/pyvenv.cfg: requirements.txt
# 	works for apt in Debian of gradescope servers, dont know about other OS's
	$(python_executable) -m venv $(environment_name) --without-pip --system-site-packages
	$(py) -m pip install -r $< --quiet

.PHONY: clean
clean:
	@rm -rf $(environment_name)
	@rm -rf __pycache__
	@rm -rf instance/stocks_data