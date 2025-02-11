install:
	pip install -r requirements.txt

lint:
	black .

run:
	fastapi dev main.py