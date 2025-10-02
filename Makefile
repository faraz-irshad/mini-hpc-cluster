.PHONY: build up down status logs clean submit monitor

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

status:
	docker compose ps

logs:
	python3 monitor_jobs.py

clean:
	docker compose down -v
	docker system prune -f
	rm -rf logs/*.log

submit:
	python3 submit_job.py

monitor:
	watch -n 2 python3 monitor_jobs.py