HOST := 0.0.0.0
PORT := 8008
IMAGE_NAME ?= shell_black_scholes
APP_NAME := $(IMAGE_NAME)
export USER ?= $(shell whoami)
TAG ?= $(USER)
BUILD_ARGS :=
run_args := -t -i --name $(APP_NAME) --rm -p $(HOST):$(PORT):$(PORT) -e HOST=$(HOST) -e PORT=$(PORT)
package_path := ./instruments/ ./market-data/ ./models/ ./securities/ ./*.py

.PHONY: all
all: build

.PHONY: build
build:
	docker build $(BUILD_ARGS) -t $(IMAGE_NAME):$(TAG) .

.PHONY: build-dev
build-dev:
	docker build $(BUILD_ARGS) -t $(IMAGE_NAME):$(TAG)-dev -f Dockerfile.dev .

.PHONY: clean-images
clean-images:
	-docker rmi -f $(IMAGE_NAME):$(TAG)

# Development mode suitable for interactive use (debugging, profiling), not for CI
.PHONY: run-dev
run-dev: build-dev
	docker run $(run_args) -v $(PWD):/shell $(IMAGE_NAME):$(TAG)-dev bash

.PHONY: run
run: build
	docker run $(run_args) $(IMAGE_NAME):$(TAG)

.PHONY: run-local
run-local:
	flask --app=pricing_engine run --host=$(HOST) --port=$(PORT)


.PHONY: lint
lint:
	pylint --ignore=./tests $(package_path)

.PHONY: clean
clean:
	rm -rf .pytest_cache ./tests/.pytest_cache ./__pycache__

.PHONY: test
test:
	pytest ./tests/test_pricing_engine.py
