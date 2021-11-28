init:
	pip3 install -r requirements.txt
build-docs:
	cd docs && make clean && sphinx-build -b html source build && cd ..
host-docs:
	cd docs/build && python3 -m http.server && cd ../..
start:
	python3 chat_bot/main.py
test:
	python -m unittest discover -v tests
pre-commit-up:
	bash tools/pre-commit/activate.sh
pre-commit-down:
	bash tools/pre-commit/deactivate.sh