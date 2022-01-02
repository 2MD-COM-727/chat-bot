init:
	pip3 install -r requirements.txt || pip install -r requirements.txt
build-docs:
	cd docs && sphinx-build -b html source build && cd ..
build-docs-clean:
	cd docs && make clean && sphinx-build -b html source build && cd ..
host-docs:
	cd docs/build && python -m http.server && cd ../..
start:
	python3 chat_bot || python chat_bot
start-admin:
	python3 chat_bot --admin || python chat_bot --admin
test:
	coverage run -m unittest discover -v chat_bot || coverage run -m unittest discover -v chat_bot
	@echo ""
	coverage report -m
host-cov:
	cd htmlcov && python -m http.server && cd ..
pre-commit-up:
	bash tools/pre-commit/activate.sh
pre-commit-down:
	bash tools/pre-commit/deactivate.sh