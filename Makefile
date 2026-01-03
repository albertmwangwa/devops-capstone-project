.PHONY: run db-create test

db-create:
flask db-create

run:
python app.py

test:
python -m pytest tests/ -v

coverage:
python -m pytest tests/ --cov=service --cov-report=html

clean:
rm -rf __pycache__
rm -rf service/__pycache__
rm -rf service/models/__pycache__
rm -rf tests/__pycache__
rm -rf .pytest_cache
rm -rf htmlcov
rm -f .coverage
