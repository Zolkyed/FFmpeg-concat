APP_NAME = src/app.py
PYTHON = python3
PIP = pip3

all: run

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(APP_NAME)

clean:
	rm -rf __pycache__ src/__pycache__ file_list.txt videos output

.PHONY: all install run clean
