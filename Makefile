init:
	pip3 install -r requirements.txt || pip install -r requirements.txt
build-docs:
	cd docs && make clean && sphinx-build -b html source build && cd ..
host-docs:
	cd docs/build && python -m http.server && cd ../..
start:
	python3 chat_bot/main.py || python chat_bot/main.py
test:
	coverage run -m unittest discover -v tests || coverage run -m unittest discover -v tests
	@echo ""
	coverage report -m
host-cov:
	cd htmlcov && python -m http.server && cd ..
pre-commit-up:
	bash tools/pre-commit/activate.sh
pre-commit-down:
	bash tools/pre-commit/deactivate.sh