init:
	pip3 install -r requirements.txt
build:
	cd docs && make clean && sphinx-build -b html source build && cd ..
host-docs:
	cd docs/build && python3 -m http.server && cd ../..
start:
	python3 chat_bot/main.py