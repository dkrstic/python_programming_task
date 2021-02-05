VENV := venv
HTTP_PORT :=

all: build

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

build: $(VENV)/bin/activate

run: build
	$(VENV)/bin/uvicorn app:app --host 0.0.0.0 --port 8000

test: build
	$(VENV)/bin/uvicorn app:app --host 0.0.0.0 --port 8000 &
	$(VENV)/bin/uvicorn app:test_app --host 0.0.0.0 --port 5000 &
	$(VENV)/bin/python3  app/test_endpoint.py &


clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete


.PHONY: all build run clean
