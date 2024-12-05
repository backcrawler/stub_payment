format:
	poetry run isort stub_payment_service/

check:
	poetry run isort stub_payment_service/ --check
	poetry run ruff stub_payment_service/
	# poetry run mypy stub_payment_service/
