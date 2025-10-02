.PHONY: build up down status logs clean submit monitor health test-failure watch-recovery

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

health:
	python3 recovery_monitor.py

test-failure:
	@echo "Testing fault tolerance..."
	@echo "Available nodes: master-node, worker-node-1, worker-node-2"
	@read -p "Enter node name to kill: " node; \
	python3 simulate_failure.py $$node

watch-recovery:
	watch -n 5 python3 recovery_monitor.py