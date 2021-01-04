clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

train:
	cd src/training && \
	python3.6 main_train.py

recognize:
	cd src/recognize &&

compose-up:
	docker-compose up --detach

compose-reup:
	docker-compose restart

compose-down:
	docker-compose stop


