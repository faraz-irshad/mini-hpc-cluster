.PHONY: build up down status logs clean submit monitor health watch-recovery prepare-data validate-model queue ansible-setup

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

status:
	docker compose ps

logs:
	python3 scripts/monitor_jobs.py

clean:
	docker compose down -v
	docker system prune -f
	rm -rf logs/*.log

submit:
	python3 scripts/submit_job.py

monitor:
	watch -n 2 python3 scripts/monitor_jobs.py

health:
	python3 scripts/recovery_monitor.py

watch-recovery:
	watch -n 5 python3 scripts/recovery_monitor.py

ansible-setup:
	ansible-playbook -i ansible/inventory.yml ansible/setup_cluster.yml

prepare-data:
	@echo "Preparing ML dataset..."
	python3 jobs/prepare_mnist.py

validate-model:
	@echo "Validating trained model..."
	python3 jobs/validate_mnist.py

queue:
	@echo "Job Queue Status:"
	python3 scripts/view_queue.py