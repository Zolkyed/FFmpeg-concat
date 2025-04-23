APP_NAME = app.py
PYTHON = python3
PIP = pip3

all: run

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(APP_NAME)

clean:
	rm -rf __pycache__ videos output file_list.txt

.PHONY: all install run clean
