
# -- Setup ----------------------------#

.PHONY: clean
clean:
	rm -rf dist/ build/ nb_py.egg* && \
	find . \( -name __pycache__ \
		-o -name "*.pyc" \
		-o -name .pytest_cache \
		-o -name .eggs \
		\) -exec rm -rf {} +\


# -- Development ----------------------#

.PHONY: test
test:
	pytest test

.PHONY: run
run:
	python nano3d/viewer.py

.PHONY: build-nanogui
build-nanogui:
	mkdir -p build_nanogui && cd build_nanogui && \
	cmake \
		-DPYTHON_EXECUTABLE:FILEPATH=`which python` \
		-DCMAKE_BUILD_TYPE=Debug \
		../ext/nanogui/ && \
	make -j4
